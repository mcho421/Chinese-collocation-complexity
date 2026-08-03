'''
    collcation extraction
'''

notHV = ['的', '吗', '吧', '呢', '啊', '呀', '之', '等']
prepositions = ['把', '被', '对', '给', '跟', '将', '为', '向', '由', '与', '和', '同']


def getColl(dependency_tree):
    collocation = []
    for token_idx, token_obj in dependency_tree.items():
        parent_idx = int(token_obj['parent'])
        if parent_idx == -1:
            continue
        parent_token = dependency_tree[parent_idx]['token']

        if token_obj['pos'] in ['wp', 'ws'] or dependency_tree[parent_idx]['pos'] in ['wp', 'ws']:
            continue

        # P_X_DN
        if token_obj['relation'] == 'POB' and token_obj['pos'] == 'nd':
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p' and parent_token in ['在', '到', '从', '自', '自从', '向',
                                                                                          '往', '除了', '于', '沿着', '至',
                                                                                          '由', '顺着', '朝', '朝着', '沿',
                                                                                          '向着']:
                coll_p_dn = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)
        if token_obj['relation'] == 'POB' and token_obj['token'] in ['时', '时候']:
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p' and parent_token in ['在', '当', '每当', '从', '自从',
                                                                                          '自', '到']:
                coll_p_dn = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)

        # P_X_U
        if token_obj['relation'] == 'RAD' and token_obj['pos'] == 'u' and token_obj['token'] not in notHV:
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p':
                coll_p_u = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_U'
                collocation.append(coll_p_u)

        # CN
        if token_obj['relation'] == 'ATT' and token_obj['pos'] == 'q':
            if dependency_tree[parent_idx]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                coll_q_n = token_obj['token'] + '\t' + parent_token + '\t' + 'Q_N'
                collocation.append(coll_q_n)
        # AN
        if token_obj['relation'] == 'ATT' and token_obj['pos'] == 'a':
            if dependency_tree[parent_idx]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                if token_idx == parent_idx - 1:
                    coll_a_n = token_obj['token'] + '\t' + parent_token + '\t' + 'A_N'
                    collocation.append(coll_a_n)
                elif token_idx == parent_idx - 2 and dependency_tree[parent_idx - 1]['token'] == '的':
                    coll_a_de_n = token_obj['token'] + '\t' + '的' + '\t' + parent_token + '\t' + 'A_DE_N'
                    collocation.append(coll_a_de_n)
                elif dependency_tree[token_idx + 1]['token'] == '的':
                    coll_a_de_x_n = token_obj['token'] + '\t' + '的' + '\t' + 'X' + '\t' + parent_token + '\t' + 'A_DE_X_N'
                    collocation.append(coll_a_de_x_n)
                elif dependency_tree[parent_idx - 1]['token'] == '的':
                    coll_a_x_de_n = token_obj['token'] + '\t' + 'X' + '\t' + '的' + '\t' + parent_token + '\t' + 'A_X_DE_N'
                    collocation.append(coll_a_x_de_n)
                else:
                    coll_a_x_n = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'A_X_N'
                    collocation.append(coll_a_x_n)

        # VO
        if token_obj['relation'] in ['VOB', 'FOB', 'IOB'] and token_obj['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
            if dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                    dependency_tree[parent_idx + 1]['token'] not in notHV:
                if dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 2]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_v_2hv_o = parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + dependency_tree[parent_idx + 2][
                        'token'] + '\t' + token_obj['token'] + '\t' + 'V_2HV_O'
                    collocation.append(coll_v_2hv_o)
                else:
                    coll_v_hv_o = parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + token_obj[
                        'token'] + '\t' + 'V_HV_O'
                    collocation.append(coll_v_hv_o)
            else:
                coll_v_o = parent_token + '\t' + token_obj['token'] + '\t' + 'V_O'
                collocation.append(coll_v_o)

        # SP
        if token_obj['relation'] == 'SBV' and token_obj['pos'] not in ['r', 'nh', 'nl']:
            if dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                    dependency_tree[parent_idx + 1]['token'] not in notHV:
                if dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 2]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_s_v_2hv = token_obj['token'] + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + \
                                   dependency_tree[parent_idx + 2]['token'] + '\t' + 'S_V_2HV'
                    collocation.append(coll_s_v_2hv)
                else:
                    coll_s_v_hv = token_obj['token'] + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + 'S_V_HV'
                    collocation.append(coll_s_v_hv)
            elif dependency_tree[parent_idx - 1]['token'] not in [':', '：']:
                coll_s_v = token_obj['token'] + '\t' + parent_token + '\t' + 'S_V'
                collocation.append(coll_s_v)

        # AP
        if token_obj['relation'] == 'ADV' and token_obj['pos'] in ['a', 'd', 'v']:
            if token_idx == parent_idx - 1:
                if dependency_tree[parent_idx]['pos'] == 'a':
                    coll_d_a = token_obj['token'] + '\t' + parent_token + '\t' + 'D_A'
                    collocation.append(coll_d_a)
                elif dependency_tree[parent_idx]['pos'] == 'v':
                    coll_d_v = token_obj['token'] + '\t' + parent_token + '\t' + 'D_V'
                    collocation.append(coll_d_v)
            elif token_idx < parent_idx and dependency_tree[token_idx + 1]['token'] == '地':
                coll_d_di_v = token_obj['token'] + '\t' + '地' + '\t' + parent_token + '\t' + 'D_DI_V'
                collocation.append(coll_d_di_v)
            elif token_idx < parent_idx:
                if dependency_tree[parent_idx]['pos'] == 'a':
                    coll_d_x_a = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'D_X_A'
                    collocation.append(coll_d_x_a)
                elif dependency_tree[parent_idx]['pos'] == 'v':
                    coll_d_x_v = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'D_X_V'
                    collocation.append(coll_d_x_v)

        # PV
        if token_obj['pos'] == 'p' and token_obj['token'] in prepositions:
            if token_obj['relation'] == 'ADV' and dependency_tree[parent_idx]['pos'] == 'v' and token_idx < parent_idx:
                if dependency_tree.__contains__(parent_idx + 1) and dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 1][
                    'relation'] in ['RAD', 'CMP'] and dependency_tree[parent_idx + 1]['token'] not in notHV and dependency_tree[parent_idx + 2][
                    'relation'] in ['RAD', 'CMP'] and dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_p_v_2hv = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + dependency_tree[parent_idx + 2]['token'] + '\t' + 'P_X_V_2HV'
                    collocation.append(coll_p_v_2hv)
                elif dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 1]['token'] not in notHV:
                    coll_p_v_hv = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + 'P_X_V_HV'
                    collocation.append(coll_p_v_hv)
                else:
                    coll_p_v = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'P_X_V'
                    collocation.append(coll_p_v)
        # PC
        if token_obj['relation'] == 'CMP':
            if token_idx == parent_idx + 1:
                if dependency_tree.__contains__(token_idx + 1):
                    if dependency_tree[token_idx + 1]['token'] in ['了', '得', '过']:
                        coll_v_c_u = parent_token + '\t' + token_obj['token'] + '\t' + dependency_tree[token_idx + 1]['token'] + '\t' + 'V_C_U'
                        collocation.append(coll_v_c_u)
                    else:
                        coll_v_c = parent_token + '\t' + token_obj['token'] + '\t' + 'V_C'
                        collocation.append(coll_v_c)
            elif token_idx == parent_idx + 2:
                if dependency_tree[token_idx - 1]['token'] in ['了', '得', '过']:
                    coll_v_u_c = parent_token + '\t' + dependency_tree[token_idx - 1]['token'] + '\t' + token_obj['token'] + '\t' + 'V_U_C'
                    collocation.append(coll_v_u_c)
                elif dependency_tree[token_idx - 1]['relation'] == 'ADV':
                    coll_v_d_c = parent_token + '\t' + dependency_tree[token_idx - 1]['token'] + '\t' + token_obj['token'] + '\t' + 'V_D_C'
                    collocation.append(coll_v_d_c)
                elif dependency_tree[token_idx - 1]['relation'] == 'ATT':
                    if dependency_tree[token_idx - 1]['pos'] == 'm':
                        coll_v_m_c = parent_token + '\t' + 'm' + '\t' + token_obj['token'] + '\t' + 'V_M_C'
                        collocation.append(coll_v_m_c)
                    else:
                        coll_v_a_c = parent_token + '\t' + 'A' + '\t' + token_obj['token'] + '\t' + 'V_A_C'
                        collocation.append(coll_v_a_c)
            elif token_idx > parent_idx + 2:
                if dependency_tree[parent_idx + 1]['token'] in ['了', '得', '过']:
                    if token_idx == parent_idx + 3:
                        if dependency_tree[token_idx - 1]['relation'] == 'ATT':
                            if dependency_tree[token_idx - 1]['pos'] == 'm':
                                coll_v_u_m_c = parent_token + '\t' + dependency_tree[token_idx - 2]['token'] + '\t' + 'm' + '\t' + token_obj[
                                    'token'] + '\t' + 'V_U_M_C'
                                collocation.append(coll_v_u_m_c)
                            else:
                                coll_v_u_a_c = parent_token + '\t' + dependency_tree[token_idx - 2]['token'] + '\t' + dependency_tree[token_idx - 1][
                                    'token'] + '\t' + token_obj['token'] + '\t' + 'V_U_A_C'
                                collocation.append(coll_v_u_a_c)
                        elif dependency_tree[token_idx - 1]['relation'] == 'ADV':
                            if token_obj['pos'] != 'v':
                                coll_v_u_d_c = parent_token + '\t' + dependency_tree[token_idx - 2]['token'] + '\t' + dependency_tree[token_idx - 1][
                                    'token'] + '\t' + token_obj['token'] + '\t' + 'V_U_D_C'
                                collocation.append(coll_v_u_d_c)
                            elif dependency_tree[token_idx + 1]['pos'] == 'wp':
                                coll_v_u_d_c = parent_token + '\t' + dependency_tree[token_idx - 2]['token'] + '\t' + dependency_tree[token_idx - 1][
                                    'token'] + '\t' + token_obj['token'] + '\t' + 'V_U_D_C'
                                collocation.append(coll_v_u_d_c)
                        else:
                            coll_v_u_x_c = parent_token + '\t' + dependency_tree[token_idx - 2]['token'] + '\t' + 'X' + '\t' + token_obj[
                                'token'] + '\t' + 'V_U_X_C'
                            collocation.append(coll_v_u_x_c)
                    else:
                        coll_v_u_x_c = parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + 'X' + '\t' + token_obj[
                            'token'] + '\t' + 'V_U_X_C'
                        collocation.append(coll_v_u_x_c)
                else:
                    coll_v_x_c = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'V_X_C'
                    collocation.append(coll_v_x_c)

    return collocation

coll_dict = {"V_O": "VO", "V_HV_O": "VO", "V_2HV_O": "VO", "D_V": "AP",
             "S_V_HV": "SP", "P_X_DN": "PP*", "V_C": "PC*",
             "S_V": "SP", "D_A": "AP", "Q_N": "CN*", "V_D_C": "PC*", "P_X_U": "PP*",
             "P_X_V": "PV*", "A_N": "AN", "A_X_DE_N": "AN", "D_X_A": "AP", "P_X_V_HV": "PV*",
             "D_X_V": "AP", "V_U_C": "PC*", "A_DE_N": "AN", "V_X_C": "PC*",
             "V_C_U": "PC*", "D_DI_V": "AP", "V_U_X_C": "PC*", "V_M_C": "PC*", "V_U_A_C": "PC*",
             "A_X_N": "AN", "V_U_D_C": "PC*", "V_U_M_C": "PC*", "A_DE_X_N": "AN",
             "P_X_V_2HV": "PV*", "S_V_2HV": "SP", "V_A_C": "PC*"}


def isUniqueColl(coll):
    typ = coll_dict[coll.split('\t')[-1]]
    if typ in ['PC*', 'PV*', 'CN*', 'PP*']:
        return True
    else:
        return False


lowfreq_colls = {line.strip():0 for line in open('./data/low_freq_coll.txt')}

def isLowFreqColl(coll):
    if coll in lowfreq_colls:
        return True
    return False