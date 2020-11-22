# -*-coding:utf-8-*-

def type_metrics(all_hanlpted_model_ners, all_hanlpted_label_ners, print_option=True):
    """
    Evaluate precision, recall and f1 score.
    :param all_hanlpted_model_ners: ner predicted by model, hanlp format ie. [[('王然', 'NR', 2, 4)], [], [('松江九亭', 'NS', 2, 6)], ...]
    :param all_hanlpted_label_ners: ner ground truth, hanlp format ie [[('王然', 'NR', 2, 4)], [], [('松江九亭', 'NS', 2, 6)], ...]
    :param print_option: whether print detailed information
    :return: list of precision, recall and f1
    """
    all_COR, all_INC, all_PAR, all_MIS, all_SPU, all_ACT, all_POS = [], [], [], [], [], [], []
    all_precision, all_recall, all_f1 = [], [], []
    for i in range(len(all_hanlpted_label_ners)):
        COR, INC, PAR, MIS, SPU = 0, 0, 0, 0, 0
        hanlpted_label_ners = all_hanlpted_label_ners[i]
        hanlpted_model_ners = all_hanlpted_model_ners[i]
        j, k = 0, 0
        if print_option:
            print()
            print('label ner:', hanlpted_label_ners)
            print('model ner:', hanlpted_model_ners)
        while j < len(hanlpted_model_ners) and k < len(hanlpted_label_ners):
            model_start_idx, model_end_idx = hanlpted_model_ners[j][2], hanlpted_model_ners[j][3]
            label_start_idx, label_end_idx = hanlpted_label_ners[k][2], hanlpted_label_ners[k][3]
            if overlap(model_start_idx, model_end_idx, label_start_idx, label_end_idx):
                model_ner = hanlpted_model_ners[j][1];
                label_ner = hanlpted_label_ners[k][1]
                j += 1;
                k += 1
                if model_ner == label_ner:
                    COR += 1
                else:
                    INC += 1
            else:
                if model_end_idx < label_end_idx:
                    j += 1;
                    SPU += 1
                else:
                    k += 1;
                    MIS += 1
        if j < len(hanlpted_model_ners):
            SPU += len(hanlpted_model_ners) - j
        if k < len(hanlpted_label_ners):
            MIS += len(hanlpted_label_ners) - k

        if len(hanlpted_model_ners) == 0 and len(hanlpted_label_ners) == 0:
            COR = 1
        all_COR.append(COR);
        all_INC.append(INC);
        all_SPU.append(SPU);
        all_MIS.append(MIS);
        all_PAR.append(PAR)
        if print_option:
            print('i={}, j={}, COR={}, INC={}, PAR={}, SPU={}, MIS={}'.format(i, j, COR, INC, PAR, SPU, MIS))
        ACT = COR + INC + PAR + SPU + 0.001;
        POS = COR + INC + PAR + MIS + 0.001
        precision = (COR + 0.5 * PAR) / ACT;
        recall = (COR + 0.5 * PAR) / POS
        f1 = 2 * precision * recall / (precision + recall + 0.001)
        all_ACT.append(ACT);
        all_POS.append(POS)
        all_precision.append(precision);
        all_recall.append(recall);
        all_f1.append(f1)
    return all_precision, all_recall, all_f1

def overlap(start_idx1, end_idx1, start_idx2, end_idx2):
    """
    Decide whether 2 intervals overlap.
    :param start_idx1:
    :param end_idx1:
    :param start_idx2:
    :param end_idx2:
    :return: True/False
    """
    head = min(end_idx1, end_idx2)
    tail = max(start_idx1, start_idx2)
    return head >= tail


if __name__ == '__main__':
    all_hanlpted_model_ners = [[('王然', 'NR', 2, 4)], [], [('松江九亭', 'NS', 2, 6)]]
    all_hanlpted_label_ners = [[('王然', 'NR', 2, 4)], [], [('松江九亭', 'NS', 2, 6)]]
    type_metrics(all_hanlpted_model_ners, all_hanlpted_label_ners, print_option=True)

