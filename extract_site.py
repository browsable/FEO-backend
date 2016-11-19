import generate_resource
import json
import urllib
import operator

def extract_data(hash_url):
    # Get json file
    arg_hash_url = hash_url
    url = "/home/refgjin/Downloads/reporter/static/wpt/"+arg_hash_url+"/data.json"
    with open(url) as d_json:
        json_data = json.load(d_json)

    #print(json_data) # probe test
    # Wrapping data into list for display through D3.js graphic renderer
    load_time=json_data['data']['runs']['1']['firstView']['loadTime']/1000
    req_cnt=json_data['data']['runs']['1']['firstView']['requestsFull']
    gzip_cnt=json_data['data']['runs']['1']['firstView']['score_gzip']
    html_siz = json_data['data']['runs']['1']['firstView']['breakdown']['html']['bytes']
    js_siz = json_data['data']['runs']['1']['firstView']['breakdown']['js']['bytes']
    css_siz = json_data['data']['runs']['1']['firstView']['breakdown']['css']['bytes']
    img_siz = json_data['data']['runs']['1']['firstView']['breakdown']['image']['bytes']
    fls_siz = json_data['data']['runs']['1']['firstView']['breakdown']['flash']['bytes']
    font_siz = json_data['data']['runs']['1']['firstView']['breakdown']['font']['bytes']
    ot_siz = json_data['data']['runs']['1']['firstView']['breakdown']['other']['bytes']
    total_rcs_siz=html_siz+js_siz+css_siz+img_siz+fls_siz+font_siz+ot_siz

    loop_cnt=0
    cdn_list=[]
    cdn_dict=dict()
    cdn_dict['Non']=0
    domain_dic=dict()
    domain_dic['Non'] = 0
    priority=None
    VeryHigh=0
    High=0
    Low=0
    Medium=0
    while(loop_cnt is not req_cnt): # Request loop
        # Get Dict a CDN_PROVIDER
        if 'cdn_provider' in json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]:
            cdnp = json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]['cdn_provider']
            if cdnp not in cdn_dict:
                cdn_dict[cdnp]=1
            else:
                cdn_dict[cdnp]=cdn_dict[cdnp]+1
        else:
            cdn_dict['Non']=cdn_dict['Non']+1
            #cdn_list.append(json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]['cdn_provider'])

        # Get a Priority
        if 'priority' in json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]:
            each_priority = json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]['priority']
            if('VeryHigh' == each_priority):
                VeryHigh=VeryHigh+1
            elif('High' == each_priority):
                High=High+1
            elif('Medium' == each_priority):
                Medium=Medium+1
            elif('Low' == each_priority):
                Low=Low+1
            else:
                print("Catcher ! Got a "+str(json_data['data']['runs']['1']['firstView']['requests'][loop_cnt]['priority']))
        loop_cnt=loop_cnt+1

    # Get Dict Domains
    if 'domains' in json_data['data']['runs']['1']['firstView']:
        domain_dic = json_data['data']['runs']['1']['firstView']['domains']

    priority=[VeryHigh, High, Medium, Low,"[ "+str(VeryHigh+High+Low+Medium)+" : "+ str(req_cnt)+"]"]

    ## CDN LIST
    # Compose cdn_list
    cdn_cnt = 0
    total_cdn_req_cnt = 0
    cdn_list = []
    for key, value in sorted(cdn_dict.items(), key=operator.itemgetter(1), reverse=True):
        tmp_list = [key, value, value]
        total_cdn_req_cnt = total_cdn_req_cnt + value
        cdn_list.append(tmp_list)
        cdn_cnt = cdn_cnt + 1

    # Calculate cdn_list's percentage
    cdn_list=calculate_percent(cdn_list,total_cdn_req_cnt)
    cdn_list.append(["Total", 100, total_cdn_req_cnt])

    ## DOMAIN LIST
    domain_s_ls=[] # domain sorted list
    domain_us_ls = [] # unsorted
    # Regenerate domain dict & list
    for k,v in domain_dic.items():
        tmp_list=[]
        requests = v['requests']
        bytes = v['bytes']
        tmp_list=[k,requests,requests,bytes]
        domain_us_ls.append(tmp_list)

    # Sorting list & Get Domain List's total request and byte
    total_domain_req_cnt = 0
    total_domain_bytes = 0
    for list in (sorted(domain_us_ls, key=lambda domain_us_ls: domain_us_ls[1], reverse=True)):
        domain_s_ls.append(list) # Add list after sort
        total_domain_req_cnt = total_domain_req_cnt + list[1]
        total_domain_bytes = total_domain_bytes + list[3]

    # Calculate domain_list's percentage
    domain_s_ls=calculate_percent(domain_s_ls,total_domain_req_cnt)
    domain_s_ls.append(["Total",100,total_domain_req_cnt,total_domain_bytes])

    # Add ',' in each bytes data
    w_cnt =0
    dom_len = len(domain_s_ls)
    domain_ls=[]
    while(w_cnt < dom_len ):
        #print(domain_s_ls[w_cnt][0])
        tmp_bytes=measuring(domain_s_ls[w_cnt][3])
        tmp_ls = [domain_s_ls[w_cnt][0], domain_s_ls[w_cnt][1], domain_s_ls[w_cnt][2], tmp_bytes]
        domain_ls.append(tmp_ls)
        w_cnt = w_cnt + 1



    """ # probe test
    load_time=str(load_time)    # Convert to string
    req_cnt=str(req_cnt)
    gzip_cnt=str(gzip_cnt)
    print("====================")
    print("WPT ID : "+json_data['data']['id'])
    print("Origin URL : " + json_data['data']['url'])
    print("Tester DNS : "+json_data['data']['testerDNS'])
    print('')

    print("Gzip count : "+gzip_cnt)
    print("Load time : "+load_time+"s")
    print("Request times : "+req_cnt)
    print("--- Resource size ---")
    print("html : "+measuring(html_siz)+" bytes, javascript : "+measuring(js_siz)+" bytes, css : "+measuring(css_siz)+" bytes, img : "+measuring(img_siz)+" bytes,")
    print(" flash : "+measuring(fls_siz)+" bytes, font : "+measuring(font_siz)+" bytes, other : "+measuring(ot_siz)+" bytes")
    print("TOTAL : "+measuring(total_rcs_siz)+" bytes")
    print("====================")
    print()

    print("CDN_PROVIDER. ")

    print(cdn_list)
    """
    #for key, value in sorted(domain_dic.items(), key=operator.itemgetter(1), reverse=True):
    #    print(" " + key + " : " + str(value))
        #dom_data[2] = ["www.domain3.xyz", 10, 5];
        #dom_data[3] = ["total", 100, 45];
    #print()
    #print("PRIORITYs,")
    #print(priority)

    return [load_time, req_cnt,gzip_cnt, priority, cdn_list, domain_ls, html_siz, js_siz, css_siz, img_siz, fls_siz, font_siz, ot_siz, total_rcs_siz]


def get_data_comparison_site(h1url, h2url, originurl):
    """ save key limits
    # Reqeust to wpt server ( Generate hash_url & Result )
    h1x_hash = generate_hash("www.facebook.com")
    h2_hash = generate_hash("www.kyobobook.co.kr")
    origin_hash = generate_hash("www.11st.co.kr")
    """
    h1x_hash = "161110_FH_24XP" # static value for test
    h2_hash = "161110_1M_24XX"
    origin_hash = "161110_G6_24XY"

    # Extract data, from h1.1, h2 & origin url to each list ( static is test value )
    #generate_resource.make_json(h1x_hash)
    h1x_list = extract_data(h1x_hash)

    #generate_resource.make_json(h2_hash)
    h2_list = extract_data(h2_hash)

    #generate_resource.make_json(origin_hash)
    origin_list = extract_data(origin_hash)


    # Generate comparison data
    return generate_data(h1x_hash,h2_hash,h1x_list,h2_list,origin_list)


def generate_data(h1x_hash,h2_hash,h1x_list,h2_list,origin_list):
    arg_h1x_hash=h1x_hash
    arg_h2_hash=h2_hash
    arg_h1x_list = h1x_list
    arg_h2_list = h2_list
    arg_origin_list = origin_list
    #[load_time, req_cnt, gzip_cnt, priority, cdn_dict, don, html_siz, js_siz, css_siz, img_siz, fls_siz, font_siz, ot_siz, total_rcs_siz]
    #      0        1        2         3          4       5      6       7       8           9       10      11        12        13

    gen_h1x=[arg_h1x_hash,arg_h1x_list[0]] # hash, load_time
    gen_h2=[arg_h2_hash,arg_h2_list[0]] # hash, load_time
    gen_org=[arg_origin_list[3],arg_origin_list[4],arg_origin_list[5]] # priority, cdn, domain

    res=[]
    #res=[arg_h1x_list[1],arg_h2_list[1],arg_h1x_list[2],arg_h2_list[2],arg_h1x_list[3],arg_h2_list[3],arg_h1x_list[4],arg_h2_list[4],arg_h1x_list[5],arg_h2_list[5],arg_h1x_list[6],arg_h2_list[6],arg_h1x_list[7],arg_h2_list[7],arg_h1x_list[8],arg_h2_list[8],arg_h1x_list[9],arg_h2_list[9],arg_h1x_list[10],arg_h2_list[10],arg_h1x_list[11],arg_h2_list[11]]

    return [gen_h1x,gen_h2,gen_org]

def generate_hash(url):
    # Generate result for request & Extract hash_url
    resp = urllib.request.urlopen(
        "http://www.webpagetest.org/runtest.php?url=" + url + "&k=A.f0ddfe447c1703ee9fae9a308b88b12a")
    resp_url = resp.geturl()  # redirect
    hash_url = resp_url.replace("http://www.webpagetest.org/result/", "")
    hash_url = hash_url.replace("/", "")
    #print(hash_url + ", " + url)  # probe test
    return hash_url

# Convert format, 10000000 to 1,000,000
def measuring(dat):
    return measuring_rc("",dat)

def measuring_rc(res,dat):
    arg_res=res
    arg_dat=dat
    if(arg_dat >= 1000):
        tmp = arg_dat // 1000
        tmp = tmp * 1000
        tmp = arg_dat - tmp
        arg_dat = arg_dat // 1000
        if (arg_res != ""):
            arg_res=","+arg_res

        str_tmp="";
        if (tmp < 10):
            str_tmp="00"+str(tmp)
        elif (tmp<100):
            str_tmp="0"+str(tmp)
        else:
            str_tmp=str(tmp)
        arg_res=str_tmp+arg_res
        return measuring_rc(arg_res,arg_dat)
    elif(arg_res != ""):
        return str(arg_dat)+","+arg_res
    else:
        return str(arg_dat)+arg_res

def calculate_percent(input_list,total_req):
    arg_list=input_list
    list_length = len(arg_list)
    while_cnt = 0
    while (while_cnt < list_length):
        arg_list[while_cnt][1] = ((arg_list[while_cnt][1] * 1000) // total_req) / 10  # unit 0.1
        # cdn_list[while_cnt][1] = (cdn_list[while_cnt][1] * 100) // total_req_cnt # unit 1
        while_cnt = while_cnt + 1

    return arg_list

# Function Test : measuring
def add_dot():
    for i in range(1,10000000):
        print(measuring(i))

#extract_data("161101_4K_10TX")
#extract_data("161110_FH_24XP")
#get_data_comparison_site()
#add_dot()
