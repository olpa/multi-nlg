import sys
import typing

import pgf

from mnlg.xbar import XMax, XType

PgfExpr = object


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

    cmd = 'UseN'
    if name.endswith('_Pron'):
        cmd = 'UsePron'
    if name.endswith('_PN'):
        cmd = 'UsePN'

    return pgf.Expr(cmd, [pgf.Expr(name, [])])


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


def vmax_to_gf(vmax: XMax) -> PgfExpr:
    gf_spec = stree_to_gf(vmax.to_spec())
    if not gf_spec:
        print('vmax_to_gf: spec is required in v-max:', vmax, file=sys.stderr)
        gf_spec = pgf.Expr('UseN', [pgf.Expr('none_N', [])])

    head = vmax.to_head()
    head = head and head.s
    if not head:
        print('vmax_to_gf: head is required in v-max:', vmax, file=sys.stderr)
        head = 'none_V'

    compl = vmax.to_complement()
    gf_compl = stree_to_gf(compl)
    if gf_compl:
        if compl.type == XType.P:
            gf_compl = pgf.Expr('CastAdvToNP', [gf_compl])
        sv = pgf.Expr('SlashV2a', [pgf.Expr(head, [])])
        gf_vp = pgf.Expr('ComplSlash', [sv, gf_compl])
    else:
        gf_vp = pgf.Expr('UseV', [pgf.Expr(head, [])])

    return pgf.Expr('PredVP', [gf_spec, gf_vp])


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
