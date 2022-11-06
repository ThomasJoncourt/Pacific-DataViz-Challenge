from PIL import Image
import cv2
import pandas as pd
import plotly.graph_objects as go
import random
import ast

def string_to_list(x):
    x = ast.literal_eval(x)
    return x

token = "pk.eyJ1IjoidGhvbWFzamN0IiwiYSI6ImNsMnN6NnVkYzAzbDczaWxya28xMTI5aW0ifQ.zFr4fMzbO2iMmBeAydU4Mg"

df_points = pd.read_csv(r"df_recensement_2019.csv")
df_cases = pd.read_csv("cases_new_caledonia.csv")

df_points["loc"] = df_points["loc"].apply(string_to_list)
df_points["points"] = df_points["points"].apply(string_to_list)

df_cases["confinement"] = False

for i in range(79,111):
    df_cases["confinement"][i] = True
for i in range(432,460):
    df_cases["confinement"][i] = True
for i in range(615,700):
    df_cases["confinement"][i] = True

j=0
l = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
points_deaths = []

for row in df_cases.index:
    print(len(points_deaths))
    print(len(l[0]))
    j += 1 
    l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13] = l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12]
    l[0] = []

    for k in range(int(df_cases.DEATH[row])):
        x = random.random()
        for row_death in df_points.index:
            if x < df_points["cumsum"][row_death]:
                p = random.sample(df_points["points"][row_death],1)[0]
                points_deaths.append(p)
                break

    for i in range(int(df_cases.CASES[row])):
        x = random.random()
        for row_cases in df_points.index:
            if x < df_points["cumsum"][row_cases]:
                p = random.sample(df_points["points"][row_cases],1)[0]
                l[0].append(p)
                break

# BIG MAP

    fig = go.Figure()

    for i in range(len(l)):

        lat = []
        long = []

        for e in l[i]:

            lat.append(e[0])
            long.append(e[1])

        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            lon = long, lat = lat,
            marker = {'size': 4, 'color':"red", "opacity":1-i/28}))
    
    lat = []
    long = []

    for e in points_deaths:

        lat.append(e[0])
        long.append(e[1])

    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = long, lat = lat,
        marker = {'size': 8, 'color':"black"}))

    if df_cases["confinement"][row] == False:

        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            lon = [166.215567], lat = [-22.016345],
            marker = {'size': 25, 'symbol': ["airport"]}))
    else:

        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            lon = [166.215567], lat = [-22.016345],
            marker = {'size': 25, 'symbol': ["prison"]}))

    fig.update_layout(mapbox_style="dark",
        mapbox_accesstoken=token,
        mapbox=dict(accesstoken=token,bearing=0,center=dict(lat=-21.2,lon=165.5),zoom=8.5),
        width=3200, 
        height=1800
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="black",
        showlegend = False)

    fig.write_image(f"img/fig_{j}_.jpeg", engine="kaleido")

# LITTLE MAP

    fig = go.Figure()

    for i in range(len(l)):

        lat = []
        long = []

        for e in l[i]:

            lat.append(e[0])
            long.append(e[1])

        fig.add_trace(go.Scattermapbox(
            mode = "markers",
            lon = long, lat = lat,
            marker = {'size': 4, 'color':"red", "opacity":1-i/28}))
    
    lat = []
    long = []

    for e in points_deaths:

        lat.append(e[0])
        long.append(e[1])

    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = long, lat = lat,
        marker = {'size': 8, 'color':"black"}))

    fig.update_layout(mapbox_style="dark",
        mapbox_accesstoken=token,
        mapbox=dict(accesstoken=token,bearing=0,center=dict(lat=-22.219459,lon=166.462212),zoom=11.3),
        width=800, 
        height=800
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="black",
        showlegend = False)

    fig.write_image(f"img/fig_little_{j}_.jpeg", engine="kaleido")

from PIL import Image

for i in range(1,1010):

    # Opening the primary image (used in background)
    img1 = Image.open(f"img/fig_little_{i}_.jpeg")
    
    # Opening the secondary image (overlay image)
    img2 = Image.open(f"img/fig_{i}_.jpeg")
    
    img2.paste(img1, (100,800))
    
    # Displaying the image
    img2.save(f'sauvegarde/img-f-{i}.jpeg', 'jpeg')

for i in range(1,1010):

    img = cv2.imread(f'sauvegarde/img-f-{i}.jpeg')

    cv2.putText(img,f'{df_cases.TIME_PERIOD[i-1]}',
        (100,500),
        cv2.FONT_HERSHEY_TRIPLEX,
        3,
        (255,255,255))

    cv2.putText(img,f'Nombre de cas actifs : {int(df_cases.CASES14[i-1])}',
        (100,600),
        cv2.FONT_HERSHEY_TRIPLEX,
        1.5,
        (0,0,255))

    cv2.putText(img,f'Nombre de cas cumules : {int(df_cases.CASES_CUMSUM[i-1])}',
        (100,650),
        cv2.FONT_HERSHEY_TRIPLEX,
        1.5,
        (0,0,255))

    cv2.putText(img,f'Nombre de deces : {int(df_cases.DEATH_CUMSUM[i-1])}',
        (100,700),
        cv2.FONT_HERSHEY_TRIPLEX,
        1.5,
        (0,0,155))

    cv2.imwrite(f'sauvegarde2/img-f-{i}.jpeg', img)