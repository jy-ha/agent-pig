import pickle
import random
import numpy as np

from apis.useful.util import debug_log


class QA_Data:
    question_ids = []

    def __init__(self):
        return

    def pickle_load(self):
        try:
            with open("apis/ap_core/probs.pickle", "rb") as file:
                self.data_tot = pickle.load(file)  # np.array(차원:답변, 행:질문, 열:메뉴) : 선택된 횟수를 가짐. 확률계산을 위해서.
            with open("apis/ap_core/probs_menu.pickle", "rb") as file:
                self.data_tot_menu = pickle.load(file)  # np.array(메뉴) : 초기확률 계산용. 선택된 횟수를 가짐.
            with open("apis/ap_core/question.pickle", "rb") as file:
                self.data_question = pickle.load(file)  # list. [(q_id, answer_num, 질문, 답변_1, _2, _3)]
            with open("apis/ap_core/menu.pickle", "rb") as file:
                self.data_menu = pickle.load(file)  # list. [(id, 메뉴, img_url) by q_id]
            with open("apis/ap_core/menu_rq.pickle", "rb") as file:
                self.menu_requested = pickle.load(file)  # list. [(메뉴, img_url)]
            self.question_ids = [q[0] for q in self.data_question]

            self.data_probs = self.data_tot / np.nansum(self.data_tot, axis=0, keepdims=True)
            self.data_probs_menu = self.data_tot_menu / self.data_tot_menu.sum()
            self.new_menus = np.argsort(self.data_tot_menu)[:len(self.data_tot_menu) // 10]
            return True
        except Exception as e:
            debug_log("ap_data_manager : pickle_load : " + str(e))
            tempdata = [
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [2, 1, 1, 1],
                    [1, 2, 1, 1],
                    [1, 1, 2, 1],
                    [1, 1, 1, 2]
                ],
                [
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ],
                [
                    [np.nan, np.nan, np.nan, np.nan],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]
                ]
            ]
            self.data_tot = np.array(tempdata)
            self.data_tot_menu = np.array([1, 1, 1, 1])
            self.data_question = [(0, 2, '술도 마심?', 'ㅇㅇ', 'ㄴㄴ', ''), (1, 3, '몇명이서 먹음?', '혼자', '2~5명', '사람 많음')]
            self.data_menu = [None, None,
                              (0, '프라이드 치킨', f"https://t1.daumcdn.net/cfile/tistory/2403BA485896A5C829"),
                              (1, '피자', f"https://cdn.dominos.co.kr/admin/upload/goods/20200311_x8StB1t3.jpg"),
                              (2, '삼겹살', f"https://cdn.mindgil.com/news/photo/202103/70839_7148_1250.jpg"),
                              (3, '족발',
                               f"https://static.hubzum.zumst.com/hubzum/2019/07/26/11/8291a05e16b14e9b91eedc7a4375c934_780x585.jpg")
                              ]
            self.menu_requested = []
            with open('apis/ap_core/probs.pickle', 'wb') as file:
                pickle.dump(self.data_tot, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/probs_menu.pickle', 'wb') as file:
                pickle.dump(self.data_tot_menu, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/question.pickle', 'wb') as file:
                pickle.dump(self.data_question, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/menu.pickle', 'wb') as file:
                pickle.dump(self.data_menu, file, pickle.HIGHEST_PROTOCOL)
            with open("apis/ap_core/menu_rq.pickle", "wb") as file:
                pickle.dump(self.menu_requested, file, pickle.HIGHEST_PROTOCOL)
            return False

    def pickle_save(self):
        try:
            with open('apis/ap_core/probs.pickle', 'wb') as file:
                pickle.dump(self.data_tot, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/probs_menu.pickle', 'wb') as file:
                pickle.dump(self.data_tot_menu, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/question.pickle', 'wb') as file:
                pickle.dump(self.data_question, file, pickle.HIGHEST_PROTOCOL)
            with open('apis/ap_core/menu.pickle', 'wb') as file:
                pickle.dump(self.data_menu, file, pickle.HIGHEST_PROTOCOL)
            return True
        except Exception as e:
            debug_log("ap_data_manager : pickle_save : " + str(e))
            return False

    def search_menu(self, id):
        # 내부 함수
        for i, menu in enumerate(self.data_menu):
            if menu != None and menu[0] == id:
                return i, menu

    def get_next(self, qa_list):
        # 제일 높은 확률의 메뉴 중, 다른 질문의 정답중, 가장 낮은 확률을 비교해서, 가장 높은 값을 갖는 질문
        try:
            if len(qa_list) == 0:
                q = random.choice(self.data_question)
                i = self.data_question.index(q)
                data = {
                    "len": q[1],
                    "q": q[2],
                    "a1": q[3],
                    "a2": q[4],
                    "a3": q[5]
                }
                return "next", int(i), -1, data

            questions = []
            prob = self.data_probs_menu
            for i, (q_i, m_i, a_i) in enumerate(qa_list):
                if q_i != -1:
                    qa_id = self.data_question[q_i][0]
                elif m_i != -1:
                    qa_id = m_i
                else:
                    return "err", -1, -1, None
                questions.append(qa_id)

                q_prob_sum = (self.data_probs[a_i, qa_id, :] * prob).sum()
                prob = (self.data_probs[a_i, qa_id, :] * prob) / q_prob_sum
                # prob = prob * (self.data_probs[a_i, qa_id, :] / 0.4)

            best_menu = np.argmax(prob)
            best_prob = prob[best_menu]
            print(f"{best_menu} {best_prob}")
            # if best_prob > 0.9:
            #    # 최종 답변으로 스킵
            #    return "final", -1, -1, None
            if best_prob > 0.1:
                i, menu = self.search_menu(best_menu)
                if i not in questions:
                    # 정답 맞추기
                    data = {
                        "name": menu[1],
                        "img_url": menu[2]
                    }
                    return "next", -1, int(i), data

            # 정답 좁히기
            qmins = np.nanmin(self.data_probs[:, :, best_menu], axis=0)
            mask = np.zeros(qmins.size, dtype=bool)
            mask[questions] = True
            qmins = np.ma.array(qmins, mask=mask)
            if qmins.size == 0:
                return "err", -1, -1, None
            best_question = np.random.choice(np.flatnonzero(np.isclose(qmins, np.max(qmins))))

            q_i, m_i = -1, -1
            data = None
            if best_question in self.question_ids:
                i = self.question_ids.index(best_question)
                q = self.data_question[i]
                q_i = i
                data = {
                    "len": q[1],
                    "q": q[2],
                    "a1": q[3],
                    "a2": q[4],
                    "a3": q[5]
                }
            else:
                m = self.data_menu[best_question]
                m_i = best_question
                data = {
                    "name": m[1],
                    "img_url": m[2]
                }
            return "next", int(q_i), int(m_i), data
        except Exception as e:
            debug_log("ap_data_manager : get_next : " + str(e))
            return "err", -1, -1, None

    def final_ask(self, qa_list):
        try:
            if len(qa_list) == 0:
                "err", -1, -1, None
            self.update(qa_list, -1)

            bad_menus = []
            prob = self.data_probs_menu
            for i, (q_i, m_i, a_i) in enumerate(qa_list):
                if q_i != -1:
                    qa_id = self.data_question[q_i][0]
                elif m_i != -1:
                    qa_id = m_i
                    if a_i == 2:
                        bad_menus.append(self.data_menu[qa_id][0])
                else:
                    return "err", None
                q_prob_sum = (self.data_probs[a_i, qa_id, :] * prob).sum()
                prob = (self.data_probs[a_i, qa_id, :] * prob) / q_prob_sum
                # prob = prob * (self.data_probs[a_i, qa_id, :] / 0.4)

            max_prob = np.max(prob)
            num_provide = 3
            best_menus_tot = []
            best_menus_new = []
            prob_argsort = np.argsort(prob)[::-1]
            i_tot, i_new = 0, 0
            for arg in prob_argsort:
                if arg not in bad_menus:
                    if (i_tot < num_provide):
                        best_menus_tot.append(arg)
                        i_tot += 1
                    elif (i_new < num_provide) and (arg in self.new_menus):
                        best_menus_new.append(arg)
                        i_new += 1
                    elif i_tot == num_provide and i_new == num_provide:
                        break
            best_probs_tot = prob[best_menus_tot]
            best_probs_new = prob[best_menus_new]

            data = {
                "a": [],
                "b": []
            }
            is_done = False
            if (len(best_probs_tot) > 0 and (best_probs_tot[0] > 0.1)) or (
                    len(best_probs_new) > 0 and (best_probs_new[0] > 0.1)):
                is_done = True
            for i, p in enumerate(best_probs_tot):
                if is_done:
                    myprob = round(p * 100, 1)
                    # myprob = round(p / max_prob * 100, 1)
                    i, menu = self.search_menu(best_menus_tot[i])
                    data["a"].append({"m_i": i, "menu": menu[1], "img_url": menu[2], "prob": myprob})
            for i, p in enumerate(best_probs_new):
                if is_done:
                    myprob = round(p * 100, 1)
                    # myprob = round(p / max_prob * 100, 1)
                    i, menu = self.search_menu(best_menus_new[i])
                    data["b"].append({"m_i": i, "menu": menu[1], "img_url": menu[2], "prob": myprob})

            if len(data["a"]) != 0 or len(data["b"]) != 0:
                return "final", data
            else:
                return "fail", data
        except Exception as e:
            debug_log("ap_data_manager : final_ask : " + str(e))
            return "err", None

    def update(self, qa_list, selected):
        try:
            if selected != -1:
                selected_i = self.data_menu[selected][0]
            for i, (q_i, m_i, a_i) in enumerate(qa_list):
                if q_i != -1:
                    qa_id = self.data_question[q_i][0]
                elif m_i != -1:
                    qa_id = m_i
                    if selected == -1:
                        other = self.data_menu[m_i][0]
                        for (q_j, m_j, a_j) in qa_list:  # 목록 메뉴들 모두 최신화
                            if q_j == q_i or m_j == m_i:
                                continue
                            if q_j != -1:
                                qa_id_j = q_j
                                if a_i == 0:
                                    self.data_tot[a_j, qa_id_j, other] += 1
                                elif a_i == 1:
                                    self.data_tot[0, qa_id_j, other] += 1
                                    if self.data_tot[2, qa_id_j, other] != np.nan:
                                        self.data_tot[2, qa_id_j, other] += 1
                                elif a_i == 2:
                                    self.data_tot[0, qa_id_j, other] += 1
                                    self.data_tot[1, qa_id_j, other] += 1
                            elif m_j != -1:
                                qa_id_j = m_j
                                if a_i == 0:
                                    self.data_tot[a_j, qa_id_j, other] += 1
                            else:
                                return -1, -1, None
                            self.data_probs[:, qa_id_j, other] = self.data_tot[:, qa_id_j, other] / np.nansum(
                                self.data_tot[:, qa_id_j, other], axis=0, keepdims=True)
                else:
                    return -1, -1, None
                if selected != -1:
                    self.data_tot[a_i, qa_id, selected_i] += 1
                    self.data_probs[:, qa_id, selected_i] = self.data_tot[:, qa_id, selected_i] / np.nansum(
                        self.data_tot[:, qa_id, selected_i], axis=0, keepdims=True)
            if selected != -1:
                self.data_tot[0, selected, selected_i] += 1  # 자기자신 괜찮음 보너스
                self.data_probs[:, selected, selected_i] = self.data_tot[:, selected, selected_i] / np.nansum(
                    self.data_tot[:, selected, selected_i], axis=0, keepdims=True)
                self.data_tot_menu[selected_i] += 1
                self.data_probs_menu = self.data_tot_menu / self.data_tot_menu.sum()
            return True
        except Exception as e:
            debug_log("ap_data_manager : update : " + str(e))
            return -1, -1, None

    def add_menu(self, name, img_url):
        try:
            if len(self.menu_requested) > 0:
                del (self.menu_requested[0])
            for i, menu in enumerate(self.data_menu):
                if menu != None and name == menu[1]:
                    self.data_menu[i] = (menu[0], name, img_url)
                    return True

            self.data_tot_menu = np.concatenate((self.data_tot_menu, np.array([1])), axis=0)
            self.data_tot = np.concatenate(
                (self.data_tot, np.full((self.data_tot.shape[0], self.data_tot.shape[1], 1), 1)), axis=2)
            self.data_tot = np.concatenate(
                (self.data_tot, np.full((self.data_tot.shape[0], 1, self.data_tot.shape[2]), 1)), axis=1)
            self.data_tot[0, -1, -1] = 2
            # 1로 초기화 하는 것보다 합리적인 방법이 있을까? -> 새 메뉴를 자꾸 무지성 추천하게 됨

            self.data_menu.append((self.data_tot.shape[2] - 1, name, img_url))
            self.data_probs = self.data_tot / np.nansum(self.data_tot, axis=0, keepdims=True)
            self.data_probs_menu = self.data_tot_menu / self.data_tot_menu.sum()

            return True
        except Exception as e:
            debug_log("ap_data_manager : add_menu : " + str(e))
            return False

    def add_menu_skip(self):
        try:
            if len(self.menu_requested) > 0:
                del (self.menu_requested[0])
            return True
        except Exception as e:
            debug_log("ap_data_manager : add_menu_skip : " + str(e))
            return False

    def add_menu_rq(self, name, img_url):
        try:
            if name == "" or name == None or img_url == "" or img_url == None:
                return "err", "정보를 입력해주세요."
            if name in map(lambda x: x[0], self.menu_requested):
                return "err", "등록 요청중인 메뉴입니다."
            if name in map(lambda x: x[1] if x != None else None, self.data_menu):
                return "err", "이미 등록된 메뉴입니다."

            self.menu_requested.append((name, img_url))
            return "ok", "신 메뉴 요청 성공!"
        except Exception as e:
            debug_log("ap_data_manager : add_menu_rq : " + str(e))
            return "err", "알 수 없는 오류가 발생했습니다."

    def get_menu_rq(self):
        try:
            if len(self.menu_requested) == 0:
                return None
            data = {
                "left": len(self.menu_requested),
                "name": self.menu_requested[0][0],
                "img_url": self.menu_requested[0][1]
            }
            return data
        except Exception as e:
            debug_log("ap_data_manager : get_menu_rq: " + str(e))
            return False

    def add_question(self, question, answers):
        try:
            new_data = np.full((self.data_tot.shape[0], 1, self.data_tot.shape[2]), 1.0)
            answers_num = 3
            if answers[2] == '':
                new_data[2, 0, :] = np.nan
                answers_num = 2
            self.data_tot = np.concatenate((self.data_tot, new_data), axis=1)
            # 1로 초기화 하는 것보다 합리적인 방법이 있을까?

            self.data_probs = self.data_tot / np.nansum(self.data_tot, axis=0, keepdims=True)
            self.data_question.append(
                (self.data_tot.shape[1] - 1, answers_num, question, answers[0], answers[1], answers[2]))
            self.question_ids.append(self.data_tot.shape[1] - 1)
            self.data_menu.append(None)
            return True
        except Exception as e:
            debug_log("ap_data_manager : add_question : " + str(e))
            return False

    def get_menu(self, m_i):
        try:
            m = self.data_menu[m_i]
            data = {
                "name": m[1],
                "img_url": m[2]
            }
            return data
        except Exception as e:
            debug_log("ap_data_manager : get_menu : " + str(e))
            return None
