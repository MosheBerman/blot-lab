import cv2,glob,numpy as np,collections,sys,os
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
pages=collections.defaultdict(list)
for f in sorted(glob.glob(f'{src}/*_overview.jpg')):
    n=os.path.basename(f).replace('_overview.jpg','')
    pages[n.rsplit('-',1)[0]].append(n)
for L,ps in pages.items():
    ovs=[cv2.imread(f'{src}/{p}_overview.jpg') for p in ps]
    h=760 if len(ps)<=2 else 560
    ovs=[cv2.resize(o,(int(o.shape[1]*h/o.shape[0]),h)) for o in ovs]
    rows=[];cur=[];w=0
    for o in ovs:
        if w+o.shape[1]>1700 and cur: rows.append(cur);cur=[];w=0
        cur.append(o);w+=o.shape[1]
    rows.append(cur)
    W=max(sum(o.shape[1] for o in r) for r in rows)
    cv2.imwrite(f'{out}/{L}_pages.jpg',np.vstack([np.hstack(r+[np.full((h,W-sum(o.shape[1] for o in r),3),255,np.uint8)]) for r in rows]),[cv2.IMWRITE_JPEG_QUALITY,78])
    for kind in ('flags','marks'):
        sh=[cv2.imread(f'{src}/{p}_{kind}.jpg') for p in ps]
        sh=[s for s in sh if s is not None]
        if not sh: continue
        Wm=max(s.shape[1] for s in sh)
        sh=np.vstack([np.hstack([s,np.full((s.shape[0],Wm-s.shape[1],3),40,np.uint8)]) for s in sh])
        for k in range(0,sh.shape[0],1680):
            cv2.imwrite(f'{out}/{L}_{kind}_{k//1680}.jpg',sh[k:k+1680],[cv2.IMWRITE_JPEG_QUALITY,80])
