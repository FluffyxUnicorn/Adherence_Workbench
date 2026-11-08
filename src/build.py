import base64
s=open('src.html').read()
lib=open('lib/xlsx.full.min.js').read()
font=base64.b64encode(open('lib/inter-latin-wght-normal.woff2','rb').read()).decode()
logo=base64.b64encode(open('assets/logo_clean.svg','rb').read()).decode()
icon=base64.b64encode(open('assets/app_icon.svg','rb').read()).decode()
for k in ['__INTER_B64__','__LOGO_B64__','__ICON_B64__','/*__XLSX__*/']: assert s.count(k)==1,k
s=s.replace('__INTER_B64__',font).replace('__LOGO_B64__',logo).replace('__ICON_B64__',icon).replace('/*__XLSX__*/',lib)
open('Adherence_Workbench.html','w').write(s)
print(len(s)//1024,'KB')
