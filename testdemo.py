import duibaSDK as sdk

url = 'https://activity.m.duiba.com.cn/autoLogin/autologin?'

tool = sdk.CreditsTool("jlg88lyxz7siqtmr", "1x0eap95f4xfi77uaptrnwh9ewzvlm")#大富翁
params = {}
params['uid']='111'
params['credits']=100

urls = tool.buildUrlWithSign(url,params)
print(urls)