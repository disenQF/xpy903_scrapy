#!/usr/bin/python3
# coding: utf-8
import random

cookies_list = [
    'acw_tc=7cc1e21615692915637732584e4d396e0a13e69460ff4e7c5a0addf4aa; QCCSESSID=2ch5rgrgqq29dh8b6e19seu124; UM_distinctid=16d61111a6c361-0df73c2105deef-38637501-75300-16d61111a6d8cd; CNZZDATA1254842228=562392532-1569291274-%7C1569291274; zg_did=%7B%22did%22%3A%20%2216d611121143ab-06835523035ae1-38637501-75300-16d61112115476%22%7D; _uab_collina=156929157592402043463238; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1569291577; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569295451287%2C%22updated%22%3A%201569296250718%2C%22info%22%3A%201569291575591%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22093f6d45452e9aad1e822e1fcf969ef0%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569296251',

]


def get():
    cookie = random.choice(cookies_list)
    return {kv.split('=')[0]: kv.split('=')[1] for kv in cookie.split(';')}
