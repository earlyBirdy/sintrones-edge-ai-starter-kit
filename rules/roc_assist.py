import numpy as np
def suggest_threshold(scores, labels, target_tpr=0.95):
    assert len(scores)==len(labels)
    order = np.argsort(scores)[::-1]
    scores = np.array(scores)[order]; labels = np.array(labels)[order]
    tp = np.cumsum(labels==1); fp = np.cumsum(labels==0); fn = tp[-1]-tp
    tpr = tp / max(tp[-1],1); precision = tp / np.maximum(tp+fp,1)
    mask = tpr >= target_tpr
    idx = np.argmax(precision*mask) if mask.any() else int(np.argmax(tpr))
    thr = float(scores[idx])
    return thr, {"tpr":float(tpr[idx]), "precision":float(precision[idx]), "fp":int(fp[idx]), "tp":int(tp[idx])}
def ab_test(current_thr, candidate_thr, scores, labels):
    import numpy as np
    scores = np.asarray(scores); labels = np.asarray(labels)
    cur = (scores>=current_thr).astype(int); cand=(scores>=candidate_thr).astype(int)
    def m(p):
        tp=((p==1)&(labels==1)).sum(); fp=((p==1)&(labels==0)).sum()
        fn=((p==0)&(labels==1)).sum(); tn=((p==0)&(labels==0)).sum()
        prec = tp/max(tp+fp,1); rec = tp/max(tp+fn,1)
        return dict(tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),precision=float(prec),recall=float(rec))
    return {"current":m(cur),"candidate":m(cand)}