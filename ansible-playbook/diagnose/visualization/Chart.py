import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Tab, Pie
from pyecharts.components import Table

Absolute_path = "/home/ansible/ansible-playbook/diagnose/result"
systems = os.popen("ls "+Absolute_path).read().split()
upservices=['Docker', 'Kubernetes', 'Podman']

for system in systems:
    find_xlsx = os.popen("find "+Absolute_path+"/"+system+" -name *.xlsx").read()
    if find_xlsx:
        dest = Absolute_path+"/"+system+"/"+system+"_result.xlsx"
        dest_ver = Absolute_path+"/"+system+"/"+system+"_verbose.xlsx"
        create_path = Absolute_path+"/"+system+"/"+system+".html"
        
        for n in range(0,len(upservices)):
            globals()["{}_xlsx".format(upservices[n])] = 1
        verbose_xlsx = 1
        
        for n in range(0,len(upservices)):
            try:
                globals()["{}_excel".format(upservices[n])] = pd.read_excel(
                    io= dest,
                    engine= "openpyxl",
                    sheet_name= upservices[n],
                    usecols= "A:H",
                    nrows= 100,
                )
                globals()["{}_check".format(upservices[n])] = globals()["{}_excel".format(upservices[n])].groupby(by=['분류']).sum()[['Good', 'Vulnerable', 'Check The Configurations']]

                globals()["bar_chart_by{}".format(upservices[n])] = (
                    Bar(init_opts=opts.InitOpts(width="1440px", height="700px"))
                    .add_xaxis(globals()["{}_check".format(upservices[n])].index.tolist())
                    .add_yaxis('Good', globals()["{}_check".format(upservices[n])]['Good'].tolist())
                    .add_yaxis('Vulnerable', globals()["{}_check".format(upservices[n])]['Vulnerable'].tolist())
                    .add_yaxis('Check The Configurations', globals()["{}_check".format(upservices[n])]['Check The Configurations'].tolist())
                    .set_colors(["#2F4554", "red", "#61A0A8"])
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=upservices[n], subtitle='chart'),
                    )
                )
            except:
                print("There is no service name: "+upservices[n]+" in "+system)
                globals()["{}_xlsx".format(upservices[n])] = 0

        try:
            Verbose_excel = pd.read_excel(
                io= dest_ver,
                engine= "openpyxl",
                sheet_name= "Verbose",
                usecols= "A:G",
                nrows= 1000,
            )

            table = Table()

            headers = ["진단 대상", "분류", "항목", "스텝", "취약한 설정 내용", "설정 방법", "점검 날짜"]
            rows=[]
            for i in range(0,len(Verbose_excel)):
                rows.append([Verbose_excel['진단 대상'][i], Verbose_excel['분류'][i], Verbose_excel['항목'][i], Verbose_excel['스텝'][i], Verbose_excel['취약한 설정 내용'][i], Verbose_excel['설정 방법'][i], Verbose_excel['점검 날짜'][i]])

            attributes={"border":"1px"}

            table.add(headers, rows)
            table.set_global_opts({"title":"Verbose","title_style":"style='color:black'"})

        except:
            print("There is no file: 'Verbose' in "+system)
            verbose_xlsx = 0

        Total = pd.read_excel(
            io= dest,
            engine= "openpyxl",
            sheet_name= "Total",
            usecols= "F:G",
            nrows= 100,
        )

        values = Total['Results']
        names = Total['Category']

        data_pair = [list(z) for z in zip(names, values)]
        
        pie_chart_total = (
            Pie(init_opts=opts.InitOpts(width="1200px", height="800px"))
            .add(
                series_name='192.168.16.36',
                data_pair=data_pair,
                center=["50%", "50%"],
                label_opts=opts.LabelOpts(is_show=True, position="center")
            )
            .set_colors(["#2F4554", "red", "#61A0A8"])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title='Total',
                    subtitle='chart',
                    title_textstyle_opts=(opts.TextStyleOpts(color="#000"))
                )
            )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

        tab = Tab(page_title=system+'_container_vulnerability')
        tab.add(pie_chart_total, 'Total')
        for n in range(0,len(upservices)):
            if globals()["{}_xlsx".format(upservices[n])] == 1:
                tab.add(globals()["bar_chart_by{}".format(upservices[n])], upservices[n])
        if verbose_xlsx == 1:
            tab.add(table, 'Verbose')
        tab.render(create_path)