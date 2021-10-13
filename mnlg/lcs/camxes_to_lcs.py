import sys
import typing
from collections.abc import Sequence

from mnlg.transform import MatchNameCondition, Rule, TransformChildren,\
    MatchName, TreeNode, NodeSet, select, SelectStep, DeepDive,\
    apply_templates, Transformer, Replace, apply_templates_iter,\
    project_children, Drop, flatten_node_sets,\
    TransformRename, Matcher, SelectStepNorm


def match_name_begin(name: str) -> Matcher:
    return MatchNameCondition(lambda node_name: node_name.startswith(name))


class SumtiAllocator:
    zohe = ['N-MAX', ['N-BAR', ['N', ['tag', "zo'e"], '']]]

    def __init__(self):
        self.sumti = []
        self.pos = 0

    def allocate_next_position(self):
        if len(self.sumti) > self.pos:
            existing = self.sumti[self.pos]
            if existing is not None:
                print('SumtiAllocator: position {} is already allocated',
                      file=sys.stderr)
        while len(self.sumti) <= self.pos:
            self.sumti.append(None)

    def push(self, node):
        if is_node_name(node, 'FA_clause'):
            self.pos = ('fa', 'fe', 'fi', 'fo', 'fu').index(node[1])
            return
        self.allocate_next_position()
        node = to_max_node(node)
        self.sumti[self.pos] = node
        self.pos += 1
        while len(self.sumti) > self.pos and self.sumti[self.pos]:
            self.pos += 1

    def push_selbri(self):
        if not len(self.sumti):
            self.pos = 1

    def get_sumti(self):
        return [node if node else SumtiAllocator.zohe for node in self.sumti]


class TransformSentence(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        camxes_bridi_tail = select(node, [
            SelectStep(DeepDive(match_name_begin('bridi_tail'))),
        ])
        camxes_i_head = select(camxes_bridi_tail, [
            SelectStep(MatchName('selbri')),
            SelectStep(MatchName('tag')),
        ])
        camxes_selbri = select(camxes_bridi_tail, [
            SelectStepNorm(MatchName('selbri')),
            SelectStepNorm(MatchName('selbri_1'))
        ])
        camxes_before_selbri = select(node, [
            SelectStep(DeepDive(match_name_begin('terms'))),
            SelectStep(MatchName('abs_term')),
        ])
        camxes_after_selbri = select(camxes_bridi_tail, [
            SelectStep(MatchName('tail_terms')),
            SelectStep(DeepDive(match_name_begin('nonabs_terms'))),
            SelectStep(DeepDive(match_name_begin('term'))),
        ])

        i_head = apply_templates_iter(rules, camxes_i_head)

        #
        # Complement
        #
        lcs_before_selbri = flatten_node_sets(map(
            lambda sumti_branch: apply_templates(rules, sumti_branch),
            camxes_before_selbri
        ))
        lcs_after_selbri = flatten_node_sets(map(
            lambda sumti_branch: apply_templates(rules, sumti_branch),
            camxes_after_selbri
        ))

        sumti = SumtiAllocator()

        for node in lcs_before_selbri:
            sumti.push(node)
        sumti.push_selbri()
        for node in lcs_after_selbri:
            sumti.push(node)

        #
        # V-BAR with V-HEAD
        #

        def rewrite_n_to_v(name_node):
            if is_node_name(name_node[0], 'N'):
                return ['V', name_node[1]]
            else:
                return name_node

        lcs_selbri = apply_templates(rules, camxes_selbri)
        lcs_selbri = list(map(rewrite_n_to_v, lcs_selbri))

        tags = [node for node in lcs_selbri if is_node_name(node, 'tag')]
        lcs_selbri = [node for node in lcs_selbri
                      if not is_node_name(node, 'tag')]

        v_max = None
        proc_tags = {}
        if not lcs_selbri:
            print('TransformSentence: no selbri among kids', file=sys.stderr)
            v_bar = ['V-FRAME']
        else:
            v = lcs_selbri.pop()
            # Code could already build V-MAX in linked sumti branch
            if is_max_node(v):
                if lcs_selbri:
                    print('TransformSentence: selbri leftover for already built V-MAX:',
                          lcs_selbri, file=sys.stderr)
                if sumti.get_sumti():
                    print('TransformSentence: sumti leftover for already built V-MAX:',
                          sumti.get_sumti(), file=sys.stderr)
                v_max = v
            else:
                proc_tags, v = split_on_processing_tags(v)
                if tags and is_node_name(v, 'V'):
                    v = [v[0], *tags, *v[1:]]
                v_bar = ['V-FRAME', v, *sumti.get_sumti()]

        while lcs_selbri:
            v = lcs_selbri.pop()
            if not is_max_node(v):
                v = ['V-MAX', ['V-FRAME', v]]
            v_bar = ['V-BAR', v_bar, v]

        spec_node = proc_tags.get('#specifier')
        if spec_node:
            spec_node = to_max_node(spec_node)
        v_spec = [spec_node] if spec_node else []

        if not v_max:
            v_max = ['V-MAX', *v_spec, v_bar]

        return [['I-MAX', ['I-BAR', ['I', *i_head], v_max]]]


def split_on_processing_tags(node: TreeNode) -> typing.Tuple[dict[str, object], TreeNode]:
    """
     Remove tags that start with hash symbol from the node.
     Return such tags and the rewritten node
    """
    tags = {}
    back_node = []
    for item in node:
        if (isinstance(item, Sequence)
                and (len(item) > 1)
                and item[0] == 'tag'
                and isinstance(item[1], str)
                and item[1].startswith('#')):
            tag_value = item[2] if len(item) > 2 else None
            tags[item[1]] = tag_value
        else:
            back_node.append(item)
    return tags, back_node


def is_node_name(node: TreeNode, name: str) -> bool:
    if not isinstance(node, Sequence):
        return False
    if not node:
        return False
    return node[0] == name


def _is_ending(node: TreeNode, ending: str) -> bool:
    if not isinstance(node, Sequence):
        return False
    if not node:
        return False
    if not isinstance(node[0], str):
        return False
    return node[0].endswith(ending)


def is_max_node(node: TreeNode) -> bool:
    return _is_ending(node, '-MAX')


def is_bar_node(node: TreeNode) -> bool:
    return _is_ending(node, '-BAR')


def to_max_node(node: TreeNode) -> TreeNode:
    if is_bar_node(node):
        max_name = f'{node[0][0]}-MAX'
        node = [max_name, node]
    return node


class TransformSumti(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if not kids:
            print('TransformSumti: no kids after transformation',
                  file=sys.stderr)
            return []
        if len(kids) > 2:
            print('TransformSumti: at most 2 kids are expected, got:',
                  kids, file=sys.stderr)
            kids = kids[:2]

        nbar = kids.pop()
        if not is_node_name(nbar, 'N-BAR'):
            print('TransformSumti: after transform,',
                  'the last kid should be N-BAR, got:',
                  nbar, file=sys.stderr)
            return []
        nmax = ['N-MAX', nbar]

        dmax = None
        if kids:
            det = kids[0]
            if is_node_name(det, 'D'):
                det = ['D', ['tag', det[1]]]
                dmax = ['D-MAX', ['D-BAR', det, nmax]]
            else:
                print('TransformSumti: after transform,',
                      'the first kid should be D-BAR, got:',
                      kids[0], file=sys.stderr)

        return [dmax or nmax]


class TransformSumti2(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if not any(is_node_name(node, 'J') for node in kids):
            return kids
        kids.insert(0, ['J', ''])
        if len(kids) % 2:
            print('With conjunction, should have even number of nodes:',
                  'pairs of (conj,x-max), got:', kids, file=sys.stderr)
            return kids

        def grouper(iterable, n):
            args = [iter(iterable)] * n
            return zip(*args)

        bar = None
        for j, xmax in grouper(kids, 2):
            if not is_node_name(j, 'J'):
                print('In (conj, x-max) pair, the first element should be',
                      'a conjunction node, got:', j, 'in the list of nodes',
                      kids, file=sys.stderr)
            if is_node_name(xmax, 'N'):  # 'je' case
                xmax = ['N-MAX', ['N-BAR', xmax]]
            else:
                xmax = to_max_node(xmax)
            if not is_max_node(xmax):
                print('In (conj, x-max) pair, the second element should be',
                      'an x-max node, got:', xmax, 'in the list of nodes',
                      kids, file=sys.stderr)

            bar_this = ['J-BAR', j, xmax]
            if bar:
                bar = ['J-BAR', bar, ['J-MAX', bar_this]]
            else:
                bar = bar_this

        return [['J-MAX', bar]]


class TransformSumtiWithRelative(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        """ produce D-BAR and N-BAR """
        # can be nested through sumti_5 and sumti_tail
        kids = apply_templates(rules, node[1:])
        relative = list(filter(lambda kid: is_node_name(kid, 'C-MAX'), kids))
        base_kids = list(filter(
            lambda kid: not is_node_name(kid, 'C-MAX'), kids))
        if len(base_kids) == 0:
            if len(relative):
                print('TransformSumtiWithRelative: no base kids, can not',
                      'attach relatives. kids are:', kids, file=sys.stderr)
            return []
        if len(base_kids) == 1:
            first_kid = base_kids[0]
            if is_max_node(first_kid):
                if len(first_kid) != 2:
                    print('TransformSumtiWithRelative: attach relatives to',
                          'X-MAX, should be without SPEC:',
                          first_kid, 'with kids:', kids, file=sys.stderr)
                    return base_kids
                first_kid = first_kid[1]  # x-bar
                base_kids = [first_kid]
        # first kid, then node name, then first letter
        bar_name = f'{base_kids[0][0][0]}-BAR'
        if len(base_kids) == 1 and is_bar_node(base_kids[0]):
            bar = base_kids[0]
        else:
            bar = [bar_name, *base_kids]
        for rel in relative:
            bar = [bar_name, bar, rel]
        return [bar]


TransformSelbri4 = TransformSumti2


class TransformRelativeClause(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        cmax = [['C-MAX', ['C-BAR', *kids]]]
        if len(kids) != 2:
            print('TransformRelativeClause: exactly two children required,'
                  f'got {len(kids)} of them:', kids, file=sys.stderr)
            return cmax
        chead, xmax = kids
        if not is_node_name(chead, 'C'):
            print('TransformRelativeClause: the first children',
                  'should be C, got:', chead, file=sys.stderr)
        elif not is_max_node(xmax):
            print('TransformRelativeClause: the second children',
                  'should be MAX, got:', xmax, file=sys.stderr)
        return cmax


class TransformLinkedSumti(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if not kids:
            return []

        # 'vomoi' gets in kids: ['tag', '#specifier', ['N-BAR', ['N', 'vo']]], 'moi']]
        processing_tags, first_node = split_on_processing_tags(kids[0])
        if len(kids) < 2 and not processing_tags:
            return kids

        if not is_node_name(first_node, 'V'):
            if not is_node_name(first_node, 'N'):
                print('TransformLintedSumti: the first child is not N or V:', first_node,
                      ', in the kids list', kids, file=sys.stderr)
                return kids
            first_node = ['V', *first_node[1:]]

        def is_expected_node(lnode):
            is_expected = (is_node_name(lnode, 'N-MAX')
                           or is_node_name(lnode, 'N-BAR')
                           or is_node_name(lnode, 'FA_clause'))
            if not is_expected:
                print('TransformLinkedSumti: expected only N-MAX and',
                      'FA_clause, got:', lnode, 'in the kids list ',
                      kids, file=sys.stderr)
            return is_expected

        if not all(map(is_expected_node, kids[1:])):
            return kids

        sumti = SumtiAllocator()
        for node in kids[1:]:
            if is_node_name(node, 'N-BAR'):
                node = ['N-MAX', node]
            sumti.push(node)

        vspec_node = processing_tags.get('#specifier')
        if vspec_node:
            vspec_node = to_max_node(vspec_node)
        vspec = [vspec_node] if vspec_node else []

        vmax = ['V-MAX', *vspec, ['V-FRAME', first_node, *sumti.get_sumti()]]

        return [vmax]


class TransformVerbWithSpecifier(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if len(kids) != 2:
            return kids
        spec_node, verb_node = kids
        if not is_node_name(verb_node, 'V'):
            return kids
        if not is_verb_with_specifier(verb_node[-1]):
            return kids
        return [['V', ['tag', '#specifier', spec_node], *verb_node[1:]]]


def is_verb_with_specifier(name):
    return name in ('moi',)


class TransformCmevla(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        word = next(iter(project_children(node)), '???')
        return [['N', ['tag', 'pn'], word]]


class TransformWord(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        word = next(iter(project_children(node)), '???')
        return [word]


class TransformKoha(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        word = next(iter(project_children(node)), '???')
        return [['N', ['tag', 'pron'], word]]


def camxes_to_lcs(tree) -> list:
    matcher_text = match_name_begin('text')
    skip_text = Rule(matcher_text, TransformChildren())
    matcher_paragraph = match_name_begin('paragraph')
    skip_paragraph = Rule(matcher_paragraph, TransformChildren())
    matcher_statement = match_name_begin('statement')
    skip_statement = Rule(matcher_statement, TransformChildren())
    rule_sentence = Rule(MatchName('sentence'), TransformSentence())
    skip_tag = Rule(MatchName('tag'), TransformChildren())
    skip_tense_modal = Rule(MatchName('tense_modal'), TransformChildren())
    skip_simple_tense_modal = Rule(MatchName('simple_tense_modal'),
                                   TransformChildren())
    skip_time = Rule(match_name_begin('time'), TransformChildren())
    rule_pu = Rule(MatchName('PU_clause'), Replace([['tag', 'pu']]))
    rule_sumti = Rule(MatchName('sumti_6'), TransformSumti())
    rule_sumti2 = Rule(MatchName('sumti_2'), TransformSumti2())
    skip_sumti = Rule(match_name_begin('sumti'), TransformChildren())
    rule_la = Rule(MatchName('LA_clause'), TransformChildren())
    drop_la = Rule(MatchName('LA'), Drop())
    rule_le = Rule(MatchName('LE_clause'), TransformRename('D'))
    drop_le = Rule(MatchName('LE'), TransformWord())
    drop_ku = Rule(MatchName('KU'), Drop())
    skip_koha = Rule(MatchName('KOhA_clause'), TransformRename('N-BAR'))
    rule_koha = Rule(MatchName('KOhA'), TransformKoha())
    rule_smevla = Rule(MatchName('cmevla'), TransformCmevla())
    rule_smevla_wrapper = Rule(MatchName('CMEVLA'), TransformChildren())
    rule_smevla_clause = Rule(MatchName('CMEVLA_clause'),
                              TransformRename('N-BAR'))
    rule_brivla = Rule(MatchName('BRIVLA'), TransformRename('N'))
    skip_brivla = Rule(match_name_begin('BRIVLA'), TransformChildren())
    rule_tanru_unit1 = Rule(MatchName('tanru_unit_1'), TransformLinkedSumti())
    rule_tanru_unit2 = Rule(MatchName('tanru_unit_2'), TransformVerbWithSpecifier())
    skip_tanru_unit = Rule(match_name_begin('tanru_unit'), TransformChildren())
    rule_lujvo = Rule(MatchName('lujvo'), TransformWord())
    rule_gismu = Rule(MatchName('gismu'), TransformWord())
    skip_selbri = Rule(match_name_begin('selbri'), TransformChildren())
    rule_selbri4 = Rule(match_name_begin('selbri_4'), TransformSelbri4())
    drop_ke_klause = Rule(MatchName('KE_clause'), Drop())
    drop_nu_klause = Rule(MatchName('NU_clause'), Drop())
    drop_kei = Rule(MatchName('KEI'), Drop())
    drop_kehe = Rule(MatchName('KEhE'), Drop())
    drop_kuho = Rule(MatchName('KUhO'), Drop())
    skip_subsentence = Rule(MatchName('subsentence'), TransformChildren())
    rule_pa_clause = Rule(MatchName('PA_clause'), TransformRename('N'))
    rule_pa = Rule(MatchName('PA'), TransformWord())
    skip_number = Rule(match_name_begin('number'), TransformRename('N-BAR'))
    rule_moi = Rule(MatchName('MOI_clause'), Replace([['V', 'moi']]))
    skip_joik = Rule(match_name_begin('joik'), TransformChildren())
    skip_jek = Rule(match_name_begin('jek'), TransformChildren())
    rule_joi_clause = Rule(MatchName('JOI_clause'), TransformRename('J'))
    rule_noi_clause = Rule(MatchName('NOI_clause'), TransformRename('C'))
    rule_ja_clause = Rule(MatchName('JA_clause'), TransformRename('J'))
    rule_joi = Rule(MatchName('JOI'), TransformWord())
    rule_noi = Rule(MatchName('NOI'), TransformWord())
    skip_term = Rule(match_name_begin('term'), TransformChildren())
    skip_abs_term = Rule(match_name_begin('abs_term'), TransformChildren())
    skip_abs_tag_term = Rule(MatchName('abs_tag_term'), TransformChildren())
    rule_fa = Rule(MatchName('FA'), TransformWord())
    rule_ja = Rule(MatchName('JA'), TransformWord())
    rule_relative_clause = Rule(MatchName('relative_clause'),
                                TransformRelativeClause())
    skip_relative_clause = Rule(match_name_begin('relative_clause'),
                                TransformChildren())
    skip_linkargs = Rule(match_name_begin('linkargs'), TransformChildren())
    skip_links = Rule(match_name_begin('links'), TransformChildren())
    drop_beho = Rule(MatchName('BEhO'), Drop())
    drop_bei = Rule(MatchName('BEI_clause'), Drop())
    rule_be_clause = Rule(MatchName('BE_clause'),
                          Replace([['FA_clause', 'fa']]))
    rule_sumti_5_with_relative = Rule(MatchName('sumti_5'),
                                      TransformSumtiWithRelative())
    rule_sumti_tail_with_relative = Rule(MatchName('sumti_tail'),
                                         TransformSumtiWithRelative())

    s_tree = apply_templates([
        skip_text, skip_paragraph, skip_statement, rule_sentence,
        skip_tag, skip_tense_modal, skip_simple_tense_modal,
        skip_time, rule_pu,
        rule_sumti_tail_with_relative, rule_sumti_5_with_relative,
        rule_sumti, rule_sumti2, skip_sumti, rule_la,
        drop_la, rule_le,
        drop_le, drop_ku,
        rule_brivla, skip_brivla,
        rule_smevla, rule_smevla_wrapper, rule_smevla_clause,
        rule_lujvo, rule_gismu,
        rule_tanru_unit1, rule_tanru_unit2, skip_tanru_unit,
        rule_selbri4, skip_selbri,
        skip_koha, rule_koha,
        drop_ke_klause, drop_nu_klause, drop_kei,
        skip_subsentence, drop_kehe,
        rule_pa_clause, rule_pa, skip_number, rule_moi,
        skip_joik, skip_jek, rule_joi, rule_joi_clause, rule_ja_clause,
        skip_abs_term, skip_abs_tag_term, skip_term,
        rule_fa, rule_ja,
        rule_noi, rule_noi_clause,
        rule_relative_clause, skip_relative_clause, drop_kuho,
        skip_linkargs, skip_links, drop_beho, drop_bei, rule_be_clause,
    ], tree)
    assert len(s_tree) == 1
    return s_tree[0]


if '__main__' == __name__:
    import json
    camxes_tree = json.load(sys.stdin)
    lcs_tree = camxes_to_lcs(camxes_tree)
    json.dump(lcs_tree, sys.stdout)
    print('')
