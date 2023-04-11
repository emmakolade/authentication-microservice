import random
import string


def generate_random_string():
    """"Generates a random string in this format koLa/olani/9784"""
    colunm1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    colunm2 = ''.join(random.choices(string.ascii_uppercase, k=5))
    number = ''.join(random.choices(string.digits, k=4))
    return f"{colunm1}/{colunm2}/{number}"


random_strings = []
for i in range(100):
    random_strings.append(generate_random_string())

print(random_strings)


STAFF_IDS = ['YCFZ/GCZBW/7816', 'KYLJ/IONGY/1871', 'XIMU/EASWB/4713', 'LOPG/JMIOH/9600', 'NLNY/HNLNY/3879', 'NNJC/UZYMS/1528', 'GQZQ/EVYSA/8654', 'RGYI/BLHPV/6495', 'WFRF/HPAZU/5887', 'BUER/MWYCI/1391', 'TAFN/NHEKI/9767', 'GWXR/QJXXB/4806', 'AAHD/JJDSH/0053', 'IEZG/RXLKW/2996', 'ZNEG/UVUVT/8550', 'UAEN/TNJNQ/5906', 'TYJC/MOEAZ/1449', 'ZFDD/ILSPP/6507', 'BJWW/SPWDO/8800', 'BGYK/XOZUP/9792', 'OFDS/IPGFS/7254', 'QOEI/NOXFZ/1764', 'KPWU/VXBVN/7264', 'TJLO/AOGQO/9775', 'MVWB/ERCSZ/5837', 'TGDO/IAJIU/5672', 'IAJA/JQZHN/0212', 'XHRI/LHVSN/1586', 'AXUM/ZWDWE/0989', 'TMLF/HTXWQ/2207', 'QUCI/XIBQD/0538', 'LGOJ/INXCJ/2697', 'VUAK/WOCST/2050', 'NBAG/EESON/8122', 'PJBZ/SLWSS/8888', 'GFVF/TAXOZ/2802', 'MBIL/XIZZH/3372', 'DAZZ/FBZAH/4969', 'DGFQ/YTCNL/7199', 'CCHH/MQIRP/5692', 'HYGT/TKATA/3702',
             'LNTC/IYGOO/4159', 'ZPVG/QHFUZ/9272', 'KPLT/WMBOX/2950', 'MCNW/XBUQL/1242', 'SFEJ/DKEGG/7403', 'NSOM/SMPWW/5512', 'CQMT/TUGLM/1468', 'TSBB/GSFTS/2456', 'GTAY/RAEHX/8024', 'FXWA/FJUAQ/6883', 'FARJ/SGAAW/0713', 'VOXU/TNOTD/6200', 'ZDBN/GBXSG/2331', 'SXFS/KGUAK/8686', 'KIAU/NGGND/4366', 'HJOE/DIRIF/7690', 'OPTE/NLIEQ/2228', 'VEPE/GXIXM/4096', 'QMQF/RMEXD/2082', 'FZED/AJDMV/3362', 'MECC/CZTXX/0423', 'RGIM/JVCXB/0936', 'TLMQ/OHPBC/4354', 'QVAE/VRVXV/3469', 'BVGK/IOJAL/9641', 'ULGY/QDHFS/9961', 'KNJM/NAIPR/0671', 'HBUE/RFKMC/6508', 'ZORV/IROIA/6239', 'IWYP/GLOAB/2746', 'VYRK/VRAVZ/7081', 'AKQN/PDPYY/5345', 'APZD/WBRGN/8150', 'OUWK/TOHFJ/6795', 'NNFU/ZSEKN/0597', 'BQFM/EIDXD/9218', 'MRDK/VKLRJ/7256', 'FLIN/OJFCK/3931', 'TXGN/KBQXK/3485', 'UQZD/MPODQ/3920', 'GDHM/MHQOF/6732', 'QGZS/HQUWD/2602', 'ECJC/PARDA/4531', 'OKGE/YSPHL/3892', 'NWFA/VQLSG/5680', 'NNAY/MMCVV/1958', 'LQJG/IJECA/0550', 'MYOM/LQJFN/9330', 'KVTT/ANDRG/3943', 'KGMC/CJOKS/2646', 'AGYH/VNBIX/0540', 'BXYJ/OQDWT/8257', 'FUAM/XMSWW/2961', 'NOWW/DPZLI/9883', 'UDXC/ACHWD/6596', 'YWWZ/APUUC/1650', 'JIJI/FWUJJ/0335', 'FNBB/BJMIV/0688', 'SFVJ/YUFWW/9446']
