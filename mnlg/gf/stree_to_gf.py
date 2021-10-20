import sys
import typing

import pgf

from mnlg.xbar import XMax, XType, XHead, XBar, XBarRec, XBarBase

PgfExpr = object


def adjunct_np_one(xmax: XMax, gf_np: PgfExpr) -> PgfExpr:
    if xmax.type != XType.P:
        print('adjunct_np_one: only P-MAX is supported', file=sys.stderr)
        return gf_np
    gf_pp = pmax_to_gf(xmax)
    if not gf_pp:
        print('adjunct_np_one: P-MAX is not converted', file=sys.stderr)
        return gf_np
    return pgf.Expr('AdvCN', [gf_np, gf_pp])


def adjunct_np(nmax: XMax, gf_np: PgfExpr) -> PgfExpr:
    for adj in nmax.to_adj():
        gf_np = adjunct_np_one(adj, gf_np)
    return gf_np


def nmax_to_gf(nmax: XMax) -> PgfExpr:
    head = nmax.to_head()
    if not head:
        print('nmax_to_gf: head is required in n-max:', nmax, file=sys.stderr)
        return None

    name = head.s
    if not name:
        print('nmax_to_gf: name is required in n-head:', nmax, head,
              file=sys.stderr)
        name = 'none_PN'

    compl = nmax.to_complement()
    if compl:
        print('nmax_to_gf: ignoring a complement:', compl,
              file=sys.stderr)

    cmd = 'UseN'
    if name.endswith('_Pron'):
        cmd = 'UsePron'
    if name.endswith('_PN'):
        cmd = 'UsePN'

    if name.endswith('_CN'):
        gf_cn = pgf.Expr(name, [])
    else:
        gf_cn = pgf.Expr(cmd, [pgf.Expr(name, [])])

    gf_cn = adjunct_np(nmax, gf_cn)
    return gf_cn


def dmax_to_gf(dmax: XMax) -> PgfExpr:
    gf_compl = stree_to_gf(dmax.to_complement())
    if not gf_compl:
        print('dmax_to_gf: complement is required in d-max:',
              dmax, file=sys.stderr)
        gf_compl = pgf.Expr('UseN', [pgf.Expr('none_N', [])])

    head = dmax.to_head()
    if not head:
        print('dmax_to_gf: head is required in d-max:', dmax, file=sys.stderr)
    tags = (dmax.to_head().tags if head else {}) or {}

    if 'mass' in tags:
        gf_mass = pgf.Expr('MassLoi', [gf_compl])
        return gf_mass

    quant = tags.get('Quant', 'IndefArt')
    num = tags.get('Num', 'NumSg')
    e_det = pgf.Expr('DetQuant', [pgf.Expr(quant, []), pgf.Expr(num, [])])
    return pgf.Expr('DetCN', [e_det, gf_compl])


def pmax_to_gf(pmax: XMax) -> PgfExpr:
    gf_compl = stree_to_gf(pmax.to_complement())
    if not gf_compl:
        print('pmax_to_gf: complement is required in p-max:',
              pmax, file=sys.stderr)
        gf_compl = dmax_to_gf(None)

    head = pmax.to_head()
    s_head = head and head.s
    if not s_head:
        print('pmax_to_gf: head is required in p-max:', pmax, file=sys.stderr)

    return pgf.Expr('PrepNP', [pgf.Expr(s_head, []), gf_compl])


def imax_to_gf(imax: XMax) -> PgfExpr:
    head = imax.to_head()
    tags = head.tags if head or head.tags else {}
    tense = tags.get('Tense', 'TPres')
    ant = tags.get('Ant', 'ASimul')
    pos = 'PPos'
    compl = imax.to_complement()
    usecl = [pgf.Expr('TTAnt', [pgf.Expr(tense, []), pgf.Expr(ant, [])]),
             pgf.Expr(pos, [])]
    if compl:
        gf_compl = stree_to_gf(compl)
        if gf_compl:
            usecl.append(gf_compl)
    return pgf.Expr('UseCl', usecl)


def is_lower_vp_shell(xmax: typing.Optional[XMax]) -> bool:
    xhead = xmax and xmax.to_head()
    return (xhead and
            xhead.type == XType.V and
            xhead.tags and
            'trace' in xhead.tags)


def head_to_gf_vn(vhead: XHead, target_vn: str) -> PgfExpr:
    sv = (vhead and vhead.s) or f'_none_{target_vn}'
    source_vn = None
    if not sv.endswith(f'_{target_vn}'):
        idx = sv.rfind('_')
        if idx > 0:
            source_vn = sv[idx+1:]
    gf_v = pgf.Expr(sv, [])
    if source_vn is not None:
        gf_v = pgf.Expr(f'Cast{source_vn}to{target_vn}', [gf_v])
    return gf_v


def head_to_gf_v(vhead: XHead) -> PgfExpr:
    return head_to_gf_vn(vhead, 'V')


def head_to_gf_v2(vhead: XHead) -> PgfExpr:
    return head_to_gf_vn(vhead, 'V2')


def vp_shell_to_gf(
        outer_vhead: XHead, outer_spec: XMax, inner_vmax: XMax
) -> PgfExpr:
    """ the structure should be already validated
    .
    Examples of linearization:
    - line VPshellDirect (CastV3toV give_V3) (UsePron i_Pron) \
      (MassNP (UseN milk_N))
    give me milk, dar me leche
    - line VPshellDirect (CastV3toV give_V3) (UsePN john_PN) \
      (MassNP (UseN milk_N))
    give John milk, dar leche a Juan (the spanish gf-rgl is smart here)
    never generated
    - line VPshell (CastV3toV give_V3) (UsePN john_PN) (MassNP (UseN milk_N))
    give milk to John, dar leche a Juan
    - line VPshell (CastV3toV sell_V3) (UsePron i_Pron) (MassNP (UseN milk_N))
    sell milk to me, vender &+ me leche (the spanish gf-rgl is smart here)
    """
    gf_subj = stree_to_gf(inner_vmax.to_spec())
    gf_compl = stree_to_gf(inner_vmax.to_complement())
    gf_v = head_to_gf_v(outer_vhead)
    subject = outer_spec.to_head()
    is_pron = (isinstance(subject, XHead) and
               subject.type == XType.N and
               subject.tags and
               'pron' in subject.tags)
    cmd = 'VPshellDirect' if is_pron else 'VPshell'
    return pgf.Expr(cmd, [gf_v, gf_subj, gf_compl])


def adjunct_pp_to_vp(pmax: XMax, gf_vp: PgfExpr) -> PgfExpr:
    head = pmax.to_head()
    s_head = head and head.s
    if not s_head:
        print('adjunct_pp_to_vp: need a P-HEAD in P-MAX',
              pmax, file=sys.stderr)
        return gf_vp

    compl = pmax.to_complement()
    if not compl:
        print('adjunct_pp_to_vp: need a complement in P-MAX',
              pmax, file=sys.stderr)
        return gf_vp

    gf_compl = stree_to_gf(compl)
    gf_adv = pgf.Expr('PrepNP', [pgf.Expr(s_head, []), gf_compl])
    return pgf.Expr('AdvVP', [gf_vp, gf_adv])


def adjunct_vp_one(xmax: XMax, gf_vp: PgfExpr) -> PgfExpr:
    if xmax.type == XType.P:
        return adjunct_pp_to_vp(xmax, gf_vp)

    if xmax.type != XType.N and xmax.type != XType.D:
        print('adjunct_vp_one: only N/D/P-MAX is supported', file=sys.stderr)
        return gf_vp
    head = xmax.to_head()
    tags = head.tags or {}

    clitic = tags.get('clitic')

    if clitic != 'indirect':
        print('adjunct_vp_one: support only:',
              'N/D-MAX indirect clitic',
              file=sys.stderr)
        return gf_vp

    if xmax.type == XType.N:
        gf_np = nmax_to_gf(xmax)
    else:
        gf_np = dmax_to_gf(xmax)

    return pgf.Expr('WithIndirectClitic', [gf_np, gf_vp])


def adjunct_vp(vmax: XMax, gf_vp: PgfExpr) -> PgfExpr:
    for adj in vmax.to_adj():
        gf_vp = adjunct_vp_one(adj, gf_vp)
    return gf_vp


def vmax_to_gf(vmax: XMax) -> PgfExpr:
    gf_spec = stree_to_gf(vmax.to_spec())
    if not gf_spec:
        print('vmax_to_gf: spec is required in v-max:', vmax, file=sys.stderr)
        gf_spec = pgf.Expr('UseN', [pgf.Expr('none_N', [])])

    head = vmax.to_head()
    if not head:
        print('vmax_to_gf: head is required in v-max:', vmax, file=sys.stderr)

    compl = vmax.to_complement()
    while True:
        if is_lower_vp_shell(compl):
            gf_vp = vp_shell_to_gf(head, compl.to_spec(), compl)
            break

        gf_compl = stree_to_gf(compl)
        if gf_compl:
            if compl.type != XType.D and compl.type != XType.N:
                print('vmax_to_gf: complement should be D/N-MAX in v-max',
                      vmax, file=sys.stderr)

        if not gf_compl:
            gf_head = head_to_gf_v(head)
            gf_vp = pgf.Expr('UseV', [gf_head])
            break

        gf_head = head_to_gf_v2(head)
        sv = pgf.Expr('SlashV2a', [gf_head])
        gf_vp = pgf.Expr('ComplSlash', [sv, gf_compl])

        break

    gf_adj_vp = adjunct_vp(vmax, gf_vp)

    return pgf.Expr('PredVP', [gf_spec, gf_adj_vp])

# --


def amax_to_gf(amax: XMax) -> PgfExpr:
    head = amax.to_head()
    s_head = (head and head.s) or 'none_A'
    return pgf.Expr('PositA', [pgf.Expr(s_head, [])])


# --

# J-conversion: two modes:
# 1. cons-mode: build gf conjunction construction
# 2. branch-mode: bring a link to the cons-mode


def jmax_to_gf_cons(jmax: XMax) -> PgfExpr:
    tag, gf = jbar_to_gf_cons(jmax.xbar)
    if tag != 'je':
        print(f'jbar_to_gf_cons_rec: unsupported conjunction {tag}',
              file=sys.stderr)
    else:
        gf = pgf.Expr('ConjAP', [pgf.Expr('and_Conj', []), gf])
    return gf


def jbar_to_gf_cons(jbar: XBar) -> typing.Tuple[str, PgfExpr]:
    if isinstance(jbar, XBarRec):
        return jbar_to_gf_cons_rec(jbar)
    return jbar_to_gf(jbar)


def jbar_to_gf_cons_rec(jbar: XBarRec) -> typing.Tuple[str, PgfExpr]:
    tag_base, gf_base = jbar_to_gf_cons(jbar.bar)
    if not isinstance(jbar.adj, XMax) or jbar.adj.type != XType.J:
        print('jbar_to_gf_cons_rec: the complement should be J-MAX, got:',
              jbar.adj, file=sys.stderr)
        return tag_base, gf_base
    tag_branch, gf_branch = jmax_to_gf_branch(jbar.adj)
    if (tag_base != '') and (tag_base != tag_branch):
        print('jbar_to_gf_cons_rec: unsupported conjunction combination:',
              f'tag base: {tag_base}, tag branch: {tag_branch}',
              file=sys.stderr)
        return tag_base, gf_base
    cons_cmd = 'ConsAP' if tag_base else 'BaseAP'
    return tag_branch, pgf.Expr(cons_cmd, [gf_base, gf_branch])


def jmax_to_gf_branch(jmax: XMax) -> typing.Tuple[str, PgfExpr]:
    if not isinstance(jmax.xbar, XBarBase):
        print('jmax_to_gf_branch: branch J-MAX should have a bar',
              'of the base type, got:', type(jmax.xbar), file=sys.stderr)
        return '', pgf.Expr('none_A', [])
    return jbar_to_gf(jmax.xbar)


def jbar_to_gf(jbar: XBarBase) -> typing.Tuple[str, PgfExpr]:
    head = jbar.head
    s_head = (head and head.s) or ''
    gf_compl = stree_to_gf(jbar.compl)
    if not gf_compl:
        print('jbar_to_gf_cons_base: a complement is required',
              file=sys.stderr)
        gf_compl = pgf.Expr('none_A', [])
    return s_head, gf_compl


# --

def stree_to_gf(stree: typing.Optional[XMax]) -> typing.Optional[PgfExpr]:
    if stree is None:
        return None
    if isinstance(stree, XMax):
        if stree.type == XType.N:
            return nmax_to_gf(stree)
        if stree.type == XType.I:
            return imax_to_gf(stree)
        if stree.type == XType.V:
            return vmax_to_gf(stree)
        if stree.type == XType.D:
            return dmax_to_gf(stree)
        if stree.type == XType.P:
            return pmax_to_gf(stree)
        if stree.type == XType.A:
            return amax_to_gf(stree)
        if stree.type == XType.J:
            return jmax_to_gf_cons(stree)
        print('stree_to_gf: TODO: unsupported X-MAX:', stree, file=sys.stderr)
        return None
    print('stree_to_gf: TODO: other than X-MAX:', stree, file=sys.stderr)
    return None


def stree_to_gf_fullstop(stree: XMax) -> PgfExpr:
    cl = stree_to_gf(stree)
    utts = pgf.Expr('UttS', [cl])
    phr = pgf.Expr('PhrUtt',
                   [pgf.Expr('NoPConj', []), utts, pgf.Expr('NoVoc', [])])
    fullstop = pgf.Expr('TFullStop', [phr, pgf.Expr('TEmpty', [])])
    return fullstop
