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

        # Skip tokens or parent tokens that are punctuation ('wp') or symbols ('ws')
        if token_obj['pos'] in ['wp', 'ws'] or dependency_tree[parent_idx]['pos'] in ['wp', 'ws']:
            continue

        # =========================================================================
        # 1. PREPOSITIONAL LOCALIZER FRAMEWORKS (P_X_DN)
        # Structure: Preposition + [Words...] + Localizer Noun (e.g., "在...上")
        # =========================================================================

        # Case 1A: Direct directional noun (e.g., 上, 下, 里) bound to a preposition parent
        if token_obj['relation'] == 'POB' and token_obj['pos'] == 'nd':
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p' and parent_token in ['在', '到', '从', '自', '自从', '向',
                                                                                          '往', '除了', '于', '沿着', '至',
                                                                                          '由', '顺着', '朝', '朝着', '沿',
                                                                                          '向着']:
                coll_p_dn = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)
        
        # Case 1B: Temporal markers (e.g., 时, 时候 / "when") bound to time-prepositions (e.g., 当...时)
        if token_obj['relation'] == 'POB' and token_obj['token'] in ['时', '时候']:
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p' and parent_token in ['在', '当', '每当', '从', '自从',
                                                                                          '自', '到']:
                coll_p_dn = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_DN'
                collocation.append(coll_p_dn)

        # =========================================================================
        # 2. PREPOSITION + AUXILIARY PATTERNS (P_X_U)
        # Structure: Preposition + [Words...] + Auxiliary Particle ('u')
        # =========================================================================
        if token_obj['relation'] == 'RAD' and token_obj['pos'] == 'u' and token_obj['token'] not in notHV:
            if token_idx > parent_idx + 1 and dependency_tree[parent_idx]['pos'] == 'p':
                coll_p_u = parent_token + '\t' + 'X' + '\t' + token_obj['token'] + '\t' + 'P_X_U'
                collocation.append(coll_p_u)

        # =========================================================================
        # 3. QUANTIFIER + NOUN (CN / Q_N)
        # Structure: Measure word/Quantifier + Noun (e.g., "一个" + "人")
        # =========================================================================
        if token_obj['relation'] == 'ATT' and token_obj['pos'] == 'q':
            if dependency_tree[parent_idx]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                coll_q_n = token_obj['token'] + '\t' + parent_token + '\t' + 'Q_N'
                collocation.append(coll_q_n)

        # =========================================================================
        # 4. ADJECTIVE + NOUN (AN / A_N)
        # Structure: Adjective modifying a Noun (Direct, via "的", or with gaps)
        # =========================================================================
        if token_obj['relation'] == 'ATT' and token_obj['pos'] == 'a':
            if dependency_tree[parent_idx]['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
                # 4A: Direct Adjective + Noun (e.g., "红花")
                if token_idx == parent_idx - 1:
                    coll_a_n = token_obj['token'] + '\t' + parent_token + '\t' + 'A_N'
                    collocation.append(coll_a_n)
                # 4B: Adjective + 的 + Noun (e.g., "红色的花")
                elif token_idx == parent_idx - 2 and dependency_tree[parent_idx - 1]['token'] == '的':
                    coll_a_de_n = token_obj['token'] + '\t' + '的' + '\t' + parent_token + '\t' + 'A_DE_N'
                    collocation.append(coll_a_de_n)
                # 4C: Adjective + 的 + [Words] + Noun
                elif dependency_tree[token_idx + 1]['token'] == '的':
                    coll_a_de_x_n = token_obj['token'] + '\t' + '的' + '\t' + 'X' + '\t' + parent_token + '\t' + 'A_DE_X_N'
                    collocation.append(coll_a_de_x_n)
                # 4D: Adjective + [Words] + 的 + Noun
                elif dependency_tree[parent_idx - 1]['token'] == '的':
                    coll_a_x_de_n = token_obj['token'] + '\t' + 'X' + '\t' + '的' + '\t' + parent_token + '\t' + 'A_X_DE_N'
                    collocation.append(coll_a_x_de_n)
                # 4E: Adjective + [Words] + Noun
                else:
                    coll_a_x_n = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'A_X_N'
                    collocation.append(coll_a_x_n)

        # =========================================================================
        # 5. VERB + OBJECT (VO)
        # Structure: Verb + (optional helper particles) + Object Noun
        # =========================================================================
        if token_obj['relation'] in ['VOB', 'FOB', 'IOB'] and token_obj['pos'] in ['n', 'ni', 'ns', 'nt', 'nz']:
            # Check if verb has trailing aspect particles (e.g., Verb + 了/过 + Object)
            if dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                    dependency_tree[parent_idx + 1]['token'] not in notHV:
                # 5A: Verb + 2 Aspect Particles + Object (e.g., 看+了+过+书)
                if dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 2]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_v_2hv_o = parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + dependency_tree[parent_idx + 2][
                        'token'] + '\t' + token_obj['token'] + '\t' + 'V_2HV_O'
                    collocation.append(coll_v_2hv_o)
                # 5B: Verb + 1 Aspect Particle + Object (e.g., 看+了+书)
                else:
                    coll_v_hv_o = parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + token_obj[
                        'token'] + '\t' + 'V_HV_O'
                    collocation.append(coll_v_hv_o)
            # 5C: Simple Verb + Object (e.g., 看书)
            else:
                coll_v_o = parent_token + '\t' + token_obj['token'] + '\t' + 'V_O'
                collocation.append(coll_v_o)

        # =========================================================================
        # 6. SUBJECT + PREDICATE / VERB (SP)
        # Structure: Subject Noun + Verb (and optional aspect particles)
        # =========================================================================
        if token_obj['relation'] == 'SBV' and token_obj['pos'] not in ['r', 'nh', 'nl']:
            # Check if the verb has attached helper particles
            if dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                    dependency_tree[parent_idx + 1]['token'] not in notHV:
                # 6A: Subject + Verb + 2 Particles
                if dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 2]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_s_v_2hv = token_obj['token'] + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1]['token'] + '\t' + \
                                   dependency_tree[parent_idx + 2]['token'] + '\t' + 'S_V_2HV'
                    collocation.append(coll_s_v_2hv)
                # 6B: Subject + Verb + 1 Particle
                else:
                    coll_s_v_hv = token_obj['token'] + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + 'S_V_HV'
                    collocation.append(coll_s_v_hv)
            # 6C: Standard Subject + Verb
            elif dependency_tree[parent_idx - 1]['token'] not in [':', '：']:
                coll_s_v = token_obj['token'] + '\t' + parent_token + '\t' + 'S_V'
                collocation.append(coll_s_v)

        # =========================================================================
        # 7. ADVERBIAL MODIFIER + PREDICATE (AP)
        # Structure: Adverb modifying an Adjective or Verb
        # =========================================================================
        if token_obj['relation'] == 'ADV' and token_obj['pos'] in ['a', 'd', 'v']:
            # 7A: Immediately adjacent Adverb + Adjective/Verb
            if token_idx == parent_idx - 1:
                if dependency_tree[parent_idx]['pos'] == 'a':
                    coll_d_a = token_obj['token'] + '\t' + parent_token + '\t' + 'D_A'
                    collocation.append(coll_d_a)
                elif dependency_tree[parent_idx]['pos'] == 'v':
                    coll_d_v = token_obj['token'] + '\t' + parent_token + '\t' + 'D_V'
                    collocation.append(coll_d_v)
            # 7B: Adverb + 地 + Verb (e.g., "认真地学习")
            elif token_idx < parent_idx and dependency_tree[token_idx + 1]['token'] == '地':
                coll_d_di_v = token_obj['token'] + '\t' + '地' + '\t' + parent_token + '\t' + 'D_DI_V'
                collocation.append(coll_d_di_v)
            # 7C: Adverb + [Words] + Adjective/Verb
            elif token_idx < parent_idx:
                if dependency_tree[parent_idx]['pos'] == 'a':
                    coll_d_x_a = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'D_X_A'
                    collocation.append(coll_d_x_a)
                elif dependency_tree[parent_idx]['pos'] == 'v':
                    coll_d_x_v = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'D_X_V'
                    collocation.append(coll_d_x_v)

        # =========================================================================
        # 8. PREPOSITIONAL VERB PHRASE (PV)
        # Structure: Prepositional phrase modifying a Verb (e.g., "从家走")
        # =========================================================================
        if token_obj['pos'] == 'p' and token_obj['token'] in prepositions:
            if token_obj['relation'] == 'ADV' and dependency_tree[parent_idx]['pos'] == 'v' and token_idx < parent_idx:
                # 8A: Preposition + [X] + Verb + 2 Aspect Particles
                if dependency_tree.__contains__(parent_idx + 1) and dependency_tree.__contains__(parent_idx + 2) and dependency_tree[parent_idx + 1][
                    'relation'] in ['RAD', 'CMP'] and dependency_tree[parent_idx + 1]['token'] not in notHV and dependency_tree[parent_idx + 2][
                    'relation'] in ['RAD', 'CMP'] and dependency_tree[parent_idx + 2]['token'] not in notHV:
                    coll_p_v_2hv = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + dependency_tree[parent_idx + 2]['token'] + '\t' + 'P_X_V_2HV'
                    collocation.append(coll_p_v_2hv)
                # 8B: Preposition + [X] + Verb + 1 Aspect Particle
                elif dependency_tree.__contains__(parent_idx + 1) and dependency_tree[parent_idx + 1]['relation'] in ['RAD', 'CMP'] and \
                        dependency_tree[parent_idx + 1]['token'] not in notHV:
                    coll_p_v_hv = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + dependency_tree[parent_idx + 1][
                        'token'] + '\t' + 'P_X_V_HV'
                    collocation.append(coll_p_v_hv)
                # 8C: Preposition + [X] + Verb
                else:
                    coll_p_v = token_obj['token'] + '\t' + 'X' + '\t' + parent_token + '\t' + 'P_X_V'
                    collocation.append(coll_p_v)

        # =========================================================================
        # 9. VERB + COMPLEMENT (PC)
        # Structure: Verb + Complement (e.g., "看" + "完" or "做" + "得" + "好")
        # =========================================================================
        if token_obj['relation'] == 'CMP':
            # 9A: Direct adjacent complement (e.g., Verb + Complement)
            if token_idx == parent_idx + 1:
                if dependency_tree.__contains__(token_idx + 1):
                    # Verb + Complement + Particle (e.g., 了/得/过)
                    if dependency_tree[token_idx + 1]['token'] in ['了', '得', '过']:
                        coll_v_c_u = parent_token + '\t' + token_obj['token'] + '\t' + dependency_tree[token_idx + 1]['token'] + '\t' + 'V_C_U'
                        collocation.append(coll_v_c_u)
                    else:
                        coll_v_c = parent_token + '\t' + token_obj['token'] + '\t' + 'V_C'
                        collocation.append(coll_v_c)
            # 9B: Verb with intervening particle or modifier before complement
            elif token_idx == parent_idx + 2:
                # Verb + Particle (了/得/过) + Complement
                if dependency_tree[token_idx - 1]['token'] in ['了', '得', '过']:
                    coll_v_u_c = parent_token + '\t' + dependency_tree[token_idx - 1]['token'] + '\t' + token_obj['token'] + '\t' + 'V_U_C'
                    collocation.append(coll_v_u_c)
                # Verb + Adverb + Complement
                elif dependency_tree[token_idx - 1]['relation'] == 'ADV':
                    coll_v_d_c = parent_token + '\t' + dependency_tree[token_idx - 1]['token'] + '\t' + token_obj['token'] + '\t' + 'V_D_C'
                    collocation.append(coll_v_d_c)
                # Verb + Quantity/Adjective Modifier + Complement
                elif dependency_tree[token_idx - 1]['relation'] == 'ATT':
                    if dependency_tree[token_idx - 1]['pos'] == 'm':
                        coll_v_m_c = parent_token + '\t' + 'm' + '\t' + token_obj['token'] + '\t' + 'V_M_C'
                        collocation.append(coll_v_m_c)
                    else:
                        coll_v_a_c = parent_token + '\t' + 'A' + '\t' + token_obj['token'] + '\t' + 'V_A_C'
                        collocation.append(coll_v_a_c)
            # 9C: Complex/Distant Complements (> 2 tokens away)
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