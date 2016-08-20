import sys
import re
import tldextract
from os.path import join, dirname, exists
import six
import codecs
import unidecode

BLACKLIST = frozenset([
    'si.edu',
    'america.edu',
    'californiacolleges.edu',
    'australia.edu',
    'cet.edu',
    'folger.edu'
])

ACADEMIC_TLDS = frozenset([
    'ac.ae',
    'ac.at',
    'ac.bd',
    'ac.be',
    'ac.cn',
    'ac.cr',
    'ac.cy',
    'ac.fj',
    'ac.gg',
    'ac.gn',
    'ac.id',
    'ac.il',
    'ac.in',
    'ac.ir',
    'ac.jp',
    'ac.ke',
    'ac.kr',
    'ac.ma',
    'ac.me',
    'ac.mu',
    'ac.mw',
    'ac.mz',
    'ac.ni',
    'ac.nz',
    'ac.om',
    'ac.pa',
    'ac.pg',
    'ac.pr',
    'ac.rs',
    'ac.ru',
    'ac.rw',
    'ac.sz',
    'ac.th',
    'ac.tz',
    'ac.ug',
    'ac.uk',
    'ac.yu',
    'ac.za',
    'ac.zm',
    'ac.zw',
    'cc.al.us',
    'cc.ar.us',
    'cc.az.us',
    'cc.ca.us',
    'cc.co.us',
    'cc.fl.us',
    'cc.ga.us',
    'cc.hi.us',
    'cc.ia.us',
    'cc.id.us',
    'cc.il.us',
    'cc.in.us',
    'cc.ks.us',
    'cc.ky.us',
    'cc.la.us',
    'cc.md.us',
    'cc.me.us',
    'cc.mi.us',
    'cc.mn.us',
    'cc.mo.us',
    'cc.ms.us',
    'cc.mt.us',
    'cc.nc.us',
    'cc.nd.us',
    'cc.ne.us',
    'cc.nj.us',
    'cc.nm.us',
    'cc.nv.us',
    'cc.ny.us',
    'cc.oh.us',
    'cc.ok.us',
    'cc.or.us',
    'cc.pa.us',
    'cc.ri.us',
    'cc.sc.us',
    'cc.sd.us',
    'cc.tx.us',
    'cc.va.us',
    'cc.vi.us',
    'cc.wa.us',
    'cc.wi.us',
    'cc.wv.us',
    'cc.wy.us',
    'ed.ao',
    'ed.cr',
    'ed.jp',
    'edu',
    'edu.af',
    'edu.al',
    'edu.ar',
    'edu.au',
    'edu.az',
    'edu.ba',
    'edu.bb',
    'edu.bd',
    'edu.bh',
    'edu.bi',
    'edu.bn',
    'edu.bo',
    'edu.br',
    'edu.bs',
    'edu.bt',
    'edu.bz',
    'edu.ck',
    'edu.cn',
    'edu.co',
    'edu.cu',
    'edu.do',
    'edu.dz',
    'edu.ec',
    'edu.ee',
    'edu.eg',
    'edu.er',
    'edu.es',
    'edu.et',
    'edu.ge',
    'edu.gh',
    'edu.gr',
    'edu.gt',
    'edu.hk',
    'edu.hn',
    'edu.ht',
    'edu.in',
    'edu.iq',
    'edu.jm',
    'edu.jo',
    'edu.kg',
    'edu.kh',
    'edu.kn',
    'edu.kw',
    'edu.ky',
    'edu.kz',
    'edu.la',
    'edu.lb',
    'edu.lr',
    'edu.lv',
    'edu.ly',
    'edu.me',
    'edu.mg',
    'edu.mk',
    'edu.ml',
    'edu.mm',
    'edu.mn',
    'edu.mo',
    'edu.mt',
    'edu.mv',
    'edu.mw',
    'edu.mx',
    'edu.my',
    'edu.ni',
    'edu.np',
    'edu.om',
    'edu.pa',
    'edu.pe',
    'edu.ph',
    'edu.pk',
    'edu.pl',
    'edu.pr',
    'edu.ps',
    'edu.pt',
    'edu.pw',
    'edu.py',
    'edu.qa',
    'edu.rs',
    'edu.ru',
    'edu.sa',
    'edu.sc',
    'edu.sd',
    'edu.sg',
    'edu.sh',
    'edu.sl',
    'edu.sv',
    'edu.sy',
    'edu.tr',
    'edu.tt',
    'edu.tw',
    'edu.ua',
    'edu.uy',
    'edu.ve',
    'edu.vn',
    'edu.ws',
    'edu.ye',
    'edu.zm',
    'es.kr',
    'g12.br',
    'hs.kr',
    'ms.kr',
    'sc.kr',
    'sc.ug',
    'sch.ae',
    'sch.gg',
    'sch.id',
    'sch.ir',
    'sch.je',
    'sch.jo',
    'sch.lk',
    'sch.ly',
    'sch.my',
    'sch.om',
    'sch.ps',
    'sch.sa',
    'sch.uk',
    'school.nz',
    'school.za',
    'tec.ar.us',
    'tec.az.us',
    'tec.co.us',
    'tec.fl.us',
    'tec.ga.us',
    'tec.ia.us',
    'tec.id.us',
    'tec.il.us',
    'tec.in.us',
    'tec.ks.us',
    'tec.ky.us',
    'tec.la.us',
    'tec.ma.us',
    'tec.md.us',
    'tec.me.us',
    'tec.mi.us',
    'tec.mn.us',
    'tec.mo.us',
    'tec.ms.us',
    'tec.mt.us',
    'tec.nc.us',
    'tec.nd.us',
    'tec.nh.us',
    'tec.nm.us',
    'tec.nv.us',
    'tec.ny.us',
    'tec.oh.us',
    'tec.ok.us',
    'tec.pa.us',
    'tec.sc.us',
    'tec.sd.us',
    'tec.tx.us',
    'tec.ut.us',
    'tec.vi.us',
    'tec.wa.us',
    'tec.wi.us',
    'tec.wv.us',
    'vic.edu.au'
])


class Swot(object):
    @classmethod
    def is_academic(cls, domain_str):
        if not domain_str or not isinstance(domain_str, six.string_types):
            return False

        domain_str = domain_str.strip().lower()
        domain = tldextract.extract(domain_str)
        if not domain.registered_domain:
            return False

        if [b for b in BLACKLIST if re.search(r'(\A|\.){0}'.format(re.escape(b)), domain_str)]:
            return False

        if domain.tld in ACADEMIC_TLDS:
            return True

        if Swot.__is_academic_domain(domain):
            return True

        return False

    @classmethod
    def __is_academic_domain(cls, domain):
        path = '{0}.txt'.format(
                join(
                        'data/lib/domains',
                        join(*reversed(domain.registered_domain.split('.')))
                )
        )

        if exists(join(dirname(__file__), path)):
            return True

        if exists(join(dirname(__file__), 'swot_data', path)):
            return True

        return False

    @classmethod
    def school_name(cls, domain_str):
        if not domain_str or not isinstance(domain_str, six.string_types):
            return 'domain error'

        domain_str = domain_str.strip().lower()
        domain = tldextract.extract(domain_str)
        if not domain.registered_domain:
            return 'domain error'

        if [b for b in BLACKLIST if re.search(r'(\A|\.){0}'.format(re.escape(b)), domain_str)]:
            return 'unknown'

        if (domain.tld in ACADEMIC_TLDS) or (Swot.__is_academic_domain(domain)):
            path = '{0}.txt'.format(
                    join(
                            'data/lib/domains',
                            join(*reversed(domain.registered_domain.split('.')))
                    )
            )
            abs_path = join(dirname(__file__), path)
            lib_path = join(dirname(__file__), 'swot_data', path)
            # print "search %s" + lib_path

            if (exists(abs_path)):
                f = codecs.open(abs_path, "r", encoding="utf-8")
                content = f.read()
                f.close
                return re.sub(r'\n', '', unidecode.unidecode(content))
            elif (exists(lib_path)):
                f = codecs.open(lib_path, "r", encoding="utf-8")
                content = f.read()
                f.close
                return re.sub(r'\n', '', unidecode.unidecode(content))
            return 'unknown'

        return 'unknown'


if __name__ == '__main__':
    #print(Swot.school_name(sys.argv[1]))
    #print(Swot.is_academic(sys.argv[1]))
