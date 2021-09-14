# From camxes parse tree to a LCS (lexical conceptual structure)
from mnlg.transform import MatchNameCondition, Rule, TransformChildren,\
    MatchName, TreeNode, NodeSet, select, SelectStep, DeepDive,\
    apply_templates, Transformer, Replace, apply_templates_iter,\
    project_children, Drop, MatchAlways, flatten_node_sets,\
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
                            ['V-BAR', ['V', *v_head], *v_compl]],
                           ]]]


class TransformSumti(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        spec = apply_templates(rules, node[1:2])
        bar = apply_templates(rules, node[2:])
        if len(spec) == 1 and next(iter(spec[0]), '') == 'N':  # KOhA
            bar = [*spec, *bar]
            spec = []
        if len(spec) == 1 and len(spec[0]) == 1:  # 'le'
            spec = spec[0]
        node = ['N-MAX']
        if spec:
            node.append(['N-SPEC', *spec])
        if bar:
            node.append(['N-BAR', *bar])
        return [node]


class TransformCmevlaClause(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        cmevla = select(node, [
            MatchAlways(), MatchName('CMEVLA'),
            MatchName('cmevla'), MatchAlways()
        ])
        cmevla = next(iter(cmevla), '???')
        return [['N', cmevla]]


class TransformWord(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        word = next(iter(project_children(node)), '???')
        return [word]


class TransformKoha(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        word = next(iter(project_children(node)), '???')
        return [['N', word]]


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
    skip_sumti = Rule(match_name_begin('sumti'), TransformChildren())
    rule_la = Rule(MatchName('LA_clause'), Drop())
    drop_la = Rule(MatchName('LA'), Drop())
    rule_le = Rule(MatchName('LE_clause'), Replace([['le']]))
    drop_le = Rule(MatchName('LE'), Drop())
    drop_ku = Rule(MatchName('KU'), Drop())
    skip_koha = Rule(MatchName('KOhA_clause'), TransformChildren())
    rule_koha = Rule(MatchName('KOhA'), TransformKoha())
    rule_smevla = Rule(MatchName('CMEVLA_clause'), TransformCmevlaClause())
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
        rule_sumti, skip_sumti, rule_la, drop_la, rule_le,
        drop_le, drop_ku,
        rule_brivla, skip_brivla,
        rule_smevla, rule_lujvo, rule_gismu,
        skip_tanru_unit, skip_selbri,
        skip_koha, rule_koha,
    ], tree)
    assert len(s_tree) == 1
    return s_tree[0]


if '__main__' == __name__:
    import json
    import sys
    camxes_tree = json.load(sys.stdin)
    lcs_tree = camxes_to_lcs(camxes_tree)
    print(lcs_tree)
