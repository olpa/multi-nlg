import sys

from mnlg.transform import MatchNameCondition, Rule, TransformChildren,\
    MatchName, TreeNode, NodeSet, select, SelectStep, DeepDive,\
    apply_templates, Transformer, Replace, apply_templates_iter,\
    project_children, Drop, flatten_node_sets,\
    TransformRename, Matcher


def match_name_begin(name: str) -> Matcher:
    return MatchNameCondition(lambda node_name: node_name.startswith(name))


class TransformSentence(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        camxes_v_spec = select(node[1], [
            SelectStep(DeepDive(match_name_begin('terms'))),
            SelectStep(DeepDive(match_name_begin('abs_term'))),
            SelectStep(MatchName('sumti')),
        ])
        camxes_bridi_tail = select(node, [
            SelectStep(DeepDive(match_name_begin('bridi_tail'))),
        ])
        camxes_i_head = select(camxes_bridi_tail, [
            SelectStep(MatchName('selbri')),
            SelectStep(MatchName('tag')),
        ])
        camxes_v_head = select(camxes_bridi_tail, [
            SelectStep(DeepDive(match_name_begin('selbri'))),
            SelectStep(DeepDive(match_name_begin('tanru'))),
        ])
        camxes_v_compl_nodes = select(camxes_bridi_tail, [
            SelectStep(MatchName('tail_terms')),
            SelectStep(DeepDive(match_name_begin('nonabs_terms'))),
            SelectStep(DeepDive(match_name_begin('term'))),
            SelectStep(DeepDive(MatchName('sumti'))),
        ])

        i_head = apply_templates_iter(rules, camxes_i_head)
        v_spec = apply_templates_iter(rules, camxes_v_spec)

        v_head = apply_templates(rules, camxes_v_head)
        v_head = map(
            lambda head: head[1] if isinstance(
                head, list) and len(head) and head[0] == 'N' else head,
            v_head
        )

        v_compl = flatten_node_sets(map(
            lambda sumti_branch: apply_templates(rules, sumti_branch),
            camxes_v_compl_nodes
        ))

        return [['I-MAX', ['I-BAR', ['I', *i_head],
                           ['V-MAX', ['V-SPEC', *v_spec],
                            ['V-FRAME', ['V', *v_head], *v_compl]],
                           ]]]


def is_node_name(node: TreeNode, name: str) -> bool:
    if not isinstance(node, list):
        return False
    if not node:
        return False
    return node[0] == name


class TransformSumti(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        kids = apply_templates(rules, node[1:])
        if not kids:
            print('TransformSumti: no kids after transformation',
                  file=sys.stderr)
            return []
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
            dbar = kids[0]
            if is_node_name(dbar, 'D-BAR'):
                dbar.append(nmax)
                dmax = ['D-MAX', dbar]
            else:
                print('TransformSumti: after transform,',
                      'the first kid should be D-BAR, got:',
                      kids[0], file=sys.stderr)

        return [dmax or nmax]


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
    rule_sumti_nbar = Rule(MatchName('sumti_tail'), TransformRename('N-BAR'))
    skip_sumti = Rule(match_name_begin('sumti'), TransformChildren())
    rule_la = Rule(MatchName('LA_clause'), TransformChildren())
    drop_la = Rule(MatchName('LA'), Drop())
    rule_le = Rule(MatchName('LE_clause'), TransformRename('D-BAR'))
    drop_le = Rule(MatchName('LE'), Replace([['D', ['tag', 'le']]]))
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

    s_tree = apply_templates([
        skip_text, skip_paragraph, skip_statement, rule_sentence,
        skip_tag, skip_tense_modal, skip_simple_tense_modal,
        skip_time, rule_pu,
        rule_sumti, rule_sumti_nbar, skip_sumti, rule_la, drop_la, rule_le,
        drop_le, drop_ku,
        rule_brivla, skip_brivla,
        rule_smevla, rule_smevla_wrapper, rule_smevla_clause,
        rule_lujvo, rule_gismu,
        skip_tanru_unit, skip_selbri,
        skip_koha, rule_koha,
    ], tree)
    assert len(s_tree) == 1
    return s_tree[0]


if '__main__' == __name__:
    import json
    camxes_tree = json.load(sys.stdin)
    lcs_tree = camxes_to_lcs(camxes_tree)
    print(lcs_tree)
