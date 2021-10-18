import collections
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
    zohe = ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], "zo'e"]]]

    def __init__(self):
        self.sumti = []
        self.pos = 0
        self.se = None

    def _allocate_next_position(self):
        if len(self.sumti) > self.pos:
            existing = self.sumti[self.pos]
            if existing is not None:
                print(f'SumtiAllocator: position {self.pos} is already'
                      'allocated, list of sumti:', self.sumti, file=sys.stderr)
        while len(self.sumti) <= self.pos:
            self.sumti.append(None)

    def push(self, node):
        if is_node_name(node, 'FA_clause'):
            self.pos = ('fa', 'fe', 'fi', 'fo', 'fu').index(node[1])
            return
        self._allocate_next_position()
        node = to_max_node(node)
        self.sumti[self.pos] = node
        self.pos += 1
        while len(self.sumti) > self.pos and self.sumti[self.pos]:
            self.pos += 1

    def push_selbri(self):
        if not len(self.sumti):
            self.pos = 1

    def push_se(self, se):
        # The constructions like 'se te klama' are possible,
        # but we ignore this corner case
        self.se = se

    def _fix_positions(self):
        if not self.se:
            return
        pos = ('none', 'se', 'te', 've', 'xe').index(self.se)
        while pos >= len(self.sumti):
            self.sumti.append(None)
        new_x1 = self.sumti[pos]
        self.sumti[pos] = self.sumti[0]
        self.sumti[0] = new_x1

    def get_sumti(self):
        self._fix_positions()
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

        selbri_parts = apply_templates(rules, camxes_selbri)
        sumti_before_selbri = flatten_node_sets(map(
            lambda sumti_branch: apply_templates(rules, sumti_branch),
            camxes_before_selbri
        ))
        sumti_after_selbri = flatten_node_sets(map(
            lambda sumti_branch: apply_templates(rules, sumti_branch),
            camxes_after_selbri
        ))

        #
        # Combine transformed children
        #

        compound_selbri = TransformSentence.group_selbri_components(
            selbri_parts
        )

        if not compound_selbri:
            print('TransformSentence: should extract selbri but have not,'
                  'from:', camxes_selbri)
            return []

        selbri_base = compound_selbri.pop()

        v_bar = TransformSentence.selbri_to_frame(
            selbri_base.v, selbri_base.tags, sumti_before_selbri,
            sumti_after_selbri, selbri_base.linked)

        adjunct = None
        for adj_selbri in compound_selbri:
            if is_max_node(adj_selbri.v):  # nu-phrase, J-MAX
                if adj_selbri.tags or adj_selbri.linked:
                    print('selbri_to_frame: X-MAX node can not be augmented.',
                          'Selbri components:', adj_selbri)
                adjunct = attach_adjunct_to_max_node(adjunct, adj_selbri.v)
                continue

            adj_frame = TransformSentence.selbri_to_frame(
                adj_selbri.v, adj_selbri.tags, [], [], adj_selbri.linked
            )
            adj_spec = []
            if adj_selbri.spec:
                adj_spec = [to_max_node(adj_selbri.spec)]
            if adjunct:
                adjunct = ['V-MAX', *adj_spec, ['V-BAR', adj_frame, adjunct]]
            else:
                adjunct = ['V-MAX', *adj_spec, adj_frame]

        v_spec = []
        if selbri_base.spec:
            v_spec = [to_max_node(selbri_base.spec)]

        if adjunct:
            v_max = ['V-MAX', *v_spec, ['V-BAR', v_bar, adjunct]]
        else:
            v_max = ['V-MAX', *v_spec, v_bar]
        return [['I-MAX', ['I-BAR', ['I', *i_head], v_max]]]

    SelbriParts = collections.namedtuple('SelbriParts', 'linked spec tags v')

    @staticmethod
    def group_selbri_components(
            selbri_list: list[TreeNode]
    ) -> list[SelbriParts]:
        # left to the verb: tags, specifier
        # right to the verb: linked arguments
        # a flag for the new group: left-material when a verb exists
        collected = []
        linked = []
        spec = None
        tags = []
        v = None

        def commit():
            nonlocal v, linked, spec, tags
            if v or linked or spec or tags:
                if not v:
                    print('group_selbri_component: selbri without v,',
                          '(linked, spec, tags, v):', (linked, spec, tags, v),
                          'in the list', selbri_list, file=sys.stderr)
                    v = ['V', '???']
                collected.append(
                    TransformSentence.SelbriParts(linked, spec, tags, v))
            linked = []
            spec = None
            tags = []
            v = None

        for item in selbri_list:
            # Right-verb material
            if is_node_name(item, 'linkargs'):
                if linked:
                    print('group_selbri_component: duplicate linkargs:',
                          item, 'in the list', selbri_list, file=sys.stderr)
                linked = item[1:]
                continue
            # Left-verb material, maybe should start a new group
            if v:
                commit()
            if is_node_name(item, '#specifier'):
                if spec:
                    print('group_selbri_component: duplicate spec:',
                          item, 'in the list', selbri_list, file=sys.stderr)
                if len(item) != 2:
                    print('group_selbri_component: spec should bring',
                          'only one node:', item, 'in the list',
                          selbri_list, file=sys.stderr)
                if len(item) > 1:
                    spec = extract_specifier(item)
                continue
            if is_node_name(item, 'tag'):
                tags.append(item)
                continue
            v = item

        commit()
        return collected

    @staticmethod
    def selbri_to_frame(verb_node: TreeNode,
                        tags: list,
                        sumti_before_selbri,
                        sumti_after_selbri, sumti_linked
                        ) -> TreeNode:
        sumti = SumtiAllocator()

        for node in sumti_before_selbri:
            sumti.push(node)
        for node in sumti_linked:
            sumti.push(node)
        sumti.push_selbri()
        for node in sumti_after_selbri:
            sumti.push(node)

        for tag in tags:
            if len(tag) == 3 and tag[1] == 'se':
                sumti.push_se(tag[2])

        (node_name, *node_compl) = verb_node
        if node_name == 'N':
            node_name = 'V'
        v = [node_name, *tags, *node_compl]
        v_bar = ['V-FRAME', v, *sumti.get_sumti()]

        return v_bar


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
    if is_max_node(node):
        return node
    node = to_bar_node(node)
    x_type = node[0][0]
    return [f'{x_type}-MAX', node]


def to_bar_node(node: TreeNode) -> TreeNode:
    if is_bar_node(node) or is_max_node(node):
        return node
    x_type = node[0][0]
    if x_type == '#':  # processing instructions
        return node
    return [f'{x_type}-BAR', node]


def extract_specifier(spec: TreeNode) -> TreeNode:
    if not is_node_name(spec, '#specifier'):
        print('extract_specifier: should be a specifier node, got:',
              spec, file=sys.stderr)
        return spec
    spec = spec[1]
    if is_bar_node(spec):
        spec = spec[1]
    return spec


def attach_adjunct_to_max_node(
        adj_node: typing.Optional[TreeNode], max_node: TreeNode
) -> TreeNode:
    if not adj_node:
        return max_node
    x_type = max_node[0][0]
    if len(max_node) == 2:
        node_name, bar_node = max_node
        return [node_name, [f'{x_type}-BAR', bar_node, adj_node]]
    if len(max_node) == 3:
        node_name, spec_node, bar_node = max_node
        return [node_name, spec_node, [f'{x_type}-BAR', bar_node, adj_node]]
    print('attach_adjunct_to_max_node: max-node representation'
          'should have 2 or 3 elements, got:', max_node)
    return max_node


def inject_tag(tag: list, node: TreeNode) -> TreeNode:
    node_name = node[0]
    if len(node_name) == 1:
        return [node_name, tag, *node[1:]]
    if not is_bar_node(node):
        print('inject_tag: if not X, then should be X-BAR, got:',
              node, file=sys.stderr)
        return node
    return [node[0], inject_tag(tag, node[1]), *node[2:]]


class TransformSumti(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        kids = list(attach_specifiers_to_sumti(kids))
        return kids


class TransformSumti6(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if not kids:
            print('TransformSumti: no kids after transformation',
                  file=sys.stderr)
            return []
        if any(map(lambda kid: is_node_name(kid, '#specifier'), kids)):
            kids = list(attach_specifiers_to_sumti(kids))
        if len(kids) > 2:
            print('TransformSumti: at most 2 kids are expected, got:',
                  kids, file=sys.stderr)
            kids = kids[:2]

        xmax = kids.pop()
        if not is_max_node(xmax):
            if not is_bar_node(xmax):
                print('TransformSumti: after transform,',
                      'the last kid should be X-MAX or X-BAR, got:',
                      xmax, file=sys.stderr)
                return []
            x_type = xmax[0][0]
            xmax = [f'{x_type}-MAX', xmax]

        dmax = None
        if kids:
            det = kids[0]
            if is_node_name(det, 'D'):
                dmax = ['D-MAX', ['D-BAR', det, xmax]]
            else:
                print('TransformSumti: after transform,',
                      'the first kid should be D-BAR, got:',
                      kids[0], file=sys.stderr)

        return [dmax or xmax]


def attach_specifiers_to_sumti(kids: list[TreeNode]) -> list[TreeNode]:
    it = iter(kids)
    try:
        while spec := next(it):
            if not is_node_name(spec, '#specifier'):
                yield spec
                continue
            spec = to_max_node(extract_specifier(spec))
            node = next(it)
            node = to_bar_node(node)
            if not is_bar_node(node):
                print('TransformSumti6.attach_specifier: need an',
                      'x-bar node, got:', node, file=sys.stderr)
            else:
                x_type = node[0][0]
                node = [f'{x_type}-MAX', spec, node]
            yield node
    except StopIteration:
        pass


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


class TransformSumti5WithRelative(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        """ produce D-BAR and N-BAR, but also X-MAX for a specifier """
        # can be nested through sumti_5 and sumti_tail
        kids = apply_templates(rules, node[1:])

        goi = list(filter(lambda kid: is_node_name(kid, 'GOI_clause'), kids))
        relative = list(filter(lambda kid: is_node_name(kid, 'C-MAX'), kids))
        quantifier = list(filter(
            lambda kid: is_node_name(kid, 'quantifier'), kids))
        base_kids = list(filter(
            lambda kid: (not (is_node_name(kid, 'C-MAX')
                              or is_node_name(kid, 'quantifier')
                              or is_node_name(kid, 'GOI_clause'))), kids))

        if not goi and not relative and not quantifier:
            return list(map(to_bar_node, kids))

        if len(base_kids) == 0:
            if len(relative) or len(quantifier):
                print('TransformSumtiWithRelative: no base kids, can not',
                      'attach relatives. kids are:', kids, file=sys.stderr)
            return []

        base = base_kids.pop()
        base = to_bar_node(base)

        if is_max_node(base):
            if len(base) != 2:
                print('TransformSumtiWithRelative: attach relatives to',
                      'X-MAX, should be without SPEC:',
                      base, 'with kids:', kids, file=sys.stderr)
                return base_kids
            base = base[1]  # x-bar

        #
        # Attach goi-tag
        # [['GOI_clause', ['N-MAX', ['N-BAR',
        #     ['N', ['tag', 'pron'], "ko'a"]]]]]
        #
        if goi:
            if len(goi) > 1:
                print('TransformSumtiWithRelative: only one goi-relative',
                      'is expected, with kids:', kids, file=sys.stderr)
            goi_tag = TransformSumti5WithRelative.get_tag_from_goi(
                goi[0][1], kids
            )
            if goi_tag:
                base = inject_tag(['tag', 'id', goi_tag], base)

        #
        # Attach adjuncts
        #
        x_type = base[0][0]
        bar_name = f'{x_type}-BAR'

        while base_kids:
            adj = base_kids.pop()
            adj = to_max_node(adj)
            base = [bar_name, base, adj]

        #
        # Attach relatives
        #
        for rel in relative:
            base = [bar_name, base, rel]

        #
        # Attach quantifier
        #
        if quantifier:
            if len(quantifier) > 1:
                print('TransformSumtiWithRelative: only one quantifier',
                      'is expected, with kids:', kids, file=sys.stderr)
            spec = to_max_node(quantifier[0][1])
            base = [f'{x_type}-MAX', spec, base]

        return [base]

    @staticmethod
    def get_tag_from_goi(
            goi_max: TreeNode, kids: list[TreeNode]
    ) -> typing.Optional[str]:
        if not is_max_node(goi_max):
            print('TransformSumtiWithRelative: the child of goi',
                  'should be X-MAX, but got:', goi_max,
                  'with kids:', kids, file=sys.stderr)
            return None
        goi_bar = goi_max[1]
        if not is_max_node(goi_max):
            print('TransformSumtiWithRelative: the child-child of goi',
                  'should be X-BAR, but got:', goi_bar,
                  'with kids:', kids, file=sys.stderr)
            return None
        goi_x = goi_bar[1]
        if not is_node_name(goi_x, 'N'):
            print('TransformSumtiWithRelative: the child-child-child of goi',
                  'should be N, but got:', goi_x,
                  'with kids:', kids, file=sys.stderr)
            return None
        goi_tag = goi_x[-1]
        if not isinstance(goi_tag, str):
            print('TransformSumtiWithRelative: the child-child-child-child',
                  'of goi should be text, but got:', goi_tag,
                  'with kids:', kids, file=sys.stderr)
            return None
        return goi_tag


TransformSelbri4 = TransformSumti2


class TransformRelativeClause(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if len(kids) != 2:
            print('TransformRelativeClause: exactly two children required,'
                  f'got {len(kids)} of them:', kids, file=sys.stderr)
            return kids
        relative, base = kids

        if is_node_name(relative, 'GOI_clause'):
            return [['GOI_clause', base]]

        cmax = [['C-MAX', ['C-BAR', *kids]]]
        if not is_node_name(relative, 'C'):
            print('TransformRelativeClause: the first children',
                  'should be C or GOI_clause, got:', relative, file=sys.stderr)
        elif not is_max_node(base):
            print('TransformRelativeClause: the second children',
                  'should be MAX, got:', base, file=sys.stderr)
        return cmax


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
        return [['#specifier', spec_node], verb_node]


def is_verb_with_specifier(name):
    return name in ('moi',)


class TransformSeTag(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if len(kids) != 1:
            print('TransformSeTag: exactly one child is expected, got:',
                  kids, file=sys.stderr)
        if not kids:
            return []
        se_tag = kids[0]
        if not isinstance(se_tag, str):
            print('TransformSeTag: the child should be a string, got:',
                  kids, file=sys.stderr)
        return [['tag', 'se', se_tag]]


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
    rule_sumti = Rule(MatchName('sumti'), TransformSumti())
    rule_sumti6 = Rule(MatchName('sumti_6'), TransformSumti6())
    rule_sumti2 = Rule(MatchName('sumti_2'), TransformSumti2())
    skip_sumti = Rule(match_name_begin('sumti_'), TransformChildren())
    rule_sumti5 = Rule(MatchName('sumti_5'), TransformSumti5WithRelative())
    rule_sumti_tail_with_relative = Rule(MatchName('sumti_tail'),
                                         TransformSumti5WithRelative())
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
    skip_tanru_unit1 = Rule(MatchName('tanru_unit_1'), TransformChildren())
    rule_tanru_unit2 = Rule(MatchName('tanru_unit_2'),
                            TransformVerbWithSpecifier())
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
    rule_goi = Rule(MatchName('GOI'), TransformWord())
    skip_term = Rule(match_name_begin('term'), TransformChildren())
    skip_abs_term = Rule(match_name_begin('abs_term'), TransformChildren())
    skip_abs_tag_term = Rule(MatchName('abs_tag_term'), TransformChildren())
    rule_fa = Rule(MatchName('FA'), TransformWord())
    rule_ja = Rule(MatchName('JA'), TransformWord())
    rule_relative_clause = Rule(MatchName('relative_clause'),
                                TransformRelativeClause())
    skip_relative_clause = Rule(match_name_begin('relative_clause'),
                                TransformChildren())
    # retain 'linkargs' as is, skip 'linkargs_N'
    skip_linkargs_n = Rule(match_name_begin('linkargs_'), TransformChildren())
    skip_links = Rule(match_name_begin('links'), TransformChildren())
    drop_beho = Rule(MatchName('BEhO'), Drop())
    drop_bei = Rule(MatchName('BEI_clause'), Drop())
    drop_be_clause = Rule(MatchName('BE_clause'), Drop())
    drop_gehu = Rule(MatchName('GEhU'), Drop())
    drop_me_clause = Rule(MatchName('ME_clause'), Drop())
    drop_mehu = Rule(MatchName('MEhU'), Drop())
    drop_boi = Rule(MatchName('BOI'), Drop())
    drop_vau = Rule(MatchName('VAU'), Drop())
    rule_se = Rule(MatchName('SE'), TransformWord())
    rule_se_clause = Rule(MatchName('SE_clause'), TransformSeTag())

    s_tree = apply_templates([
        skip_text, skip_paragraph, skip_statement, rule_sentence,
        skip_tag, skip_tense_modal, skip_simple_tense_modal,
        skip_time, rule_pu,
        rule_sumti_tail_with_relative, rule_sumti5,
        rule_sumti, rule_sumti6, rule_sumti2, skip_sumti, rule_la,
        drop_la, rule_le,
        drop_le, drop_ku,
        rule_brivla, skip_brivla,
        rule_smevla, rule_smevla_wrapper, rule_smevla_clause,
        rule_lujvo, rule_gismu,
        skip_tanru_unit1, rule_tanru_unit2, skip_tanru_unit,
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
        skip_linkargs_n,
        skip_links, drop_beho, drop_bei, drop_be_clause,
        drop_gehu, rule_goi,
        drop_me_clause, drop_mehu, drop_vau,
        drop_boi,
        rule_se, rule_se_clause,
    ], tree)
    assert len(s_tree) == 1
    return s_tree[0]


if '__main__' == __name__:
    import json
    camxes_tree = json.load(sys.stdin)
    lcs_tree = camxes_to_lcs(camxes_tree)
    json.dump(lcs_tree, sys.stdout)
    print('')
