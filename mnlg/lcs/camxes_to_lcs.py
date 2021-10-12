import sys
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

        if not lcs_selbri:
            print('TransformSentence: no selbri among kids', file=sys.stderr)
            v_bar = ['V-FRAME']
        else:
            v = lcs_selbri.pop()
            if tags and is_node_name(v, 'V'):
                v = [v[0], *tags, *v[1:]]
            v_bar = ['V-FRAME', v, *sumti.get_sumti()]

        while lcs_selbri:
            v = lcs_selbri.pop()
            if not is_max_node(v):
                v = ['V-MAX', ['V-FRAME', v]]
            v_bar = ['V-BAR', v_bar, v]

        return [['I-MAX', ['I-BAR', ['I', *i_head],
                           ['V-MAX', v_bar],
                           ]]]


def is_node_name(node: TreeNode, name: str) -> bool:
    if not isinstance(node, Sequence):
        return False
    if not node:
        return False
    return node[0] == name


def is_max_node(node: TreeNode) -> bool:
    if not isinstance(node, Sequence):
        return False
    if not node:
        return False
    if not isinstance(node[0], str):
        return False
    return node[0].endswith('-MAX')


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


class TransformSumtiTail(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        relative = filter(lambda kid: is_node_name(kid, 'C-MAX'), kids)
        base = filter(lambda kid: not is_node_name(kid, 'C-MAX'), kids)
        bar = ['N-BAR', *base]
        for rel in relative:
            bar = ['N-BAR', bar, rel]
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
            print('TransformRelativeClause: the first children should be C, got:',
                  chead, file=sys.stderr)
        elif not is_max_node(xmax):
            print('TransformRelativeClause: the second children should be MAX, got:',
                  xmax, file=sys.stderr)
        return cmax


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
    rule_sumti_nbar = Rule(MatchName('sumti_tail'), TransformSumtiTail())
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
    rule_pa_clause = Rule(MatchName('PA_clause'), TransformRename('V'))
    rule_pa = Rule(MatchName('PA'), TransformWord())
    skip_number = Rule(match_name_begin('number'), TransformChildren())
    rule_moi = Rule(MatchName('MOI_clause'), Replace([['tag', 'moi']]))
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
    rule_relative_clause = Rule(MatchName('relative_clause'), TransformRelativeClause())
    skip_relative_clause = Rule(match_name_begin('relative_clause'), TransformChildren())

    s_tree = apply_templates([
        skip_text, skip_paragraph, skip_statement, rule_sentence,
        skip_tag, skip_tense_modal, skip_simple_tense_modal,
        skip_time, rule_pu,
        rule_sumti, rule_sumti2, rule_sumti_nbar, skip_sumti, rule_la,
        drop_la, rule_le,
        drop_le, drop_ku,
        rule_brivla, skip_brivla,
        rule_smevla, rule_smevla_wrapper, rule_smevla_clause,
        rule_lujvo, rule_gismu,
        skip_tanru_unit,
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
    ], tree)
    assert len(s_tree) == 1
    return s_tree[0]


if '__main__' == __name__:
    import json
    camxes_tree = json.load(sys.stdin)
    lcs_tree = camxes_to_lcs(camxes_tree)
    json.dump(lcs_tree, sys.stdout)
    print('')
