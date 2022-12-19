from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import openpyxl
import base64
#from plotly.subplots import make_subplots
import pathlib




df_strategy = pd.read_excel('სტრატეგია.xlsx')
df_fuel_consumption = pd.read_excel('საწვავის მოხამრება.xlsx')
df_emmision = pd.read_excel('სათბურუ_გაზების_ემისია.xlsx')
df_ex_sankey = pd.read_excel('საწვავლის_მოხმარება_სანკი.xlsx')
df_auto_park_fuel = pd.read_excel('ავტოპარკი_საწვავის_ტიპი.xlsx')
df_auto_park_age = pd.read_excel('ავტოპარკი_ასაკი.xlsx')
df_auto_park_type = pd.read_excel('ავტოპარკი_ავტ_ტიპი.xlsx')
df_world_emmision = pd.read_excel('მსოფლიო ემისიები ქვეყნების მიხედვით.xls')


image_filename_car = 'car1.png'
encoded_image_car = base64.b64encode(open(image_filename_car, 'rb').read()).decode('ascii')
image_filename_fuel = 'download.png'
encoded_image_fuel = base64.b64encode(open(image_filename_fuel, 'rb').read()).decode('ascii')

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server



# padding for the page content
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
}

top_line = html.Div([
html.Br(),
    html.H4("საქართველოს სატრანსპორტო სექტორის მიმოხილვა და მასთან დაკავშირებული კლიმატის გამოწვევები")
    ], style={'font-family': 'Akademiuri', "padding" : "10px", "font-weight": "bold"}
)
middle_line = html.Div([
html.Br(),
html.Br(),
html.Br(),
    html.H4("პრობლემის გადაჭრის გზები")
    ], style={'font-family': 'Akademiuri', "padding" : "10px"}
)
#sidebar = html.Div(
    #[
       # html.H2("სატრანსპორტო სექტორი და მისი გავლენა კლიმატის ცვლილებაზე", className="lead", style=  {'font-family': 'Akademiuri','font-weight' : 'bold', "font-size": "20px"},),
        #html.Hr(),
       # html.Br(),
        #html.Br(),
        #dbc.Nav(
         #   [

          #      dbc.NavLink("სატრანსპორტო სექტორი და კლიმატის გამოწვევები", href="/page-1", active="exact"),
           #     html.Br(),
            #    dbc.NavLink("გადაჭრის გზები", href="/page-2", active="exact"),

            #],
            #vertical=True,
            #pills=True,
            #style={"font-size": "20px", 'font-family': 'Akademiuri'}
        #),
    #],
    #style=SIDEBAR_STYLE,
#)


#content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)






figm= go.Figure()
figm.add_trace(go.Bar(x=df_emmision['თარიღი'], y=df_emmision['სხვა სექტორები'], name='სხვა სექტორები',  marker_color= '#607EAA'))
figm.add_trace(go.Bar(x=df_emmision['თარიღი'], y=df_emmision['ტრანსპორტი'], name='ტრანსპორტი', marker_color= '#EAE509'))
figm.update_layout(template="simple_white", barmode='stack', margin = dict(l=40, b=60, t=0, pad=20))
figm.update_layout(legend=dict(
    y=0.88,
    x=0.1,
    traceorder="normal"
))
figm.update_layout(xaxis=dict(
                showgrid=False,
                tickangle=45,
    type = "category", dtick=3
            ))
figm.update_layout(font=dict(size=15)
            )


####
unique_source_target = list(pd.unique(df_ex_sankey[['source', 'target']].values.ravel('K')))

mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
df_ex_sankey['source'] = df_ex_sankey['source'].map(mapping_dict)
df_ex_sankey['target'] = df_ex_sankey['target'].map(mapping_dict)

links_dict = df_ex_sankey.to_dict(orient='list')

figs = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 10,
      line = dict(color = "black", width = 1),
      label = unique_source_target,
      color = "black"
    ),
    link = dict(
      source = links_dict["source"],
      target = links_dict["target"],
      value = links_dict["value"],
      color = px.colors.sequential.GnBu
  ))])
figs.update_traces(legendrank=1000, selector=dict(type='sankey'))
figs.update_traces(textfont_size=20, selector=dict(type='sankey'))
 ####


### cars type###
fign= go.Figure(go.Bar(x=df_auto_park_type["წლები"], y=df_auto_park_type["სატვირთო"], name="სატვირთო",  marker_color= '#c3bad7'))
fign.add_trace(go.Bar(x=df_auto_park_type["წლები"], y=df_auto_park_type["ავტობუსი და მიკროავტობუსები"], name="ავტობუსი და მიკროავტობუსები",  marker_color= '#EAE509'))
fign.add_trace(go.Bar(x=df_auto_park_type["წლები"], y=df_auto_park_type["სპეციალური"], name="სპეციალური",  marker_color= '#a6bed3'))
fign.add_trace(go.Bar(x=df_auto_park_type["წლები"], y=df_auto_park_type[ "მსუბუქი"], name="მსუბუქი",  marker_color="#607EAA"))
fign.update_layout(barmode='stack')
fign.update_layout(template="simple_white")
fign.update_layout(legend=dict(
    y=0.99,
    orientation="h",
    yanchor ="bottom",
    xanchor= "left"
))

##### car_age
figg=go.Figure()
figg.add_trace(go.Scatter(x=df_auto_park_age["წელი"], y=df_auto_park_age["<= 2 წელი"],
                    mode='lines+markers',
                    name='<= 2 წელი'))
figg.add_trace(go.Scatter(x=df_auto_park_age["წელი"], y=df_auto_park_age["<= 5 წელი"],
                    mode='lines+markers',
                    name='<= 5 წელი', marker_color="#a6bed3"))
figg.add_trace(go.Scatter(x=df_auto_park_age["წელი"], y=df_auto_park_age["<= 10 წელი"],
                    mode='lines+markers',
                    name='<= 10 წელი', marker_color="#EAE509"))
figg.add_trace(go.Scatter(x=df_auto_park_age["წელი"], y=df_auto_park_age["> 10 წელი"],
                    mode='lines+markers',
                    name='> 10 წელი', marker_color="#c3bad7"))
figg.add_trace(go.Scatter(x=df_auto_park_age["წელი"], y=df_auto_park_age["უცნობია"],
                    mode='lines+markers',
                    name='უცნობია', marker_color="#fda47b"))
figg.update_layout(template="simple_white")
figg.update_layout(
    title="")
figg.update_layout(legend= dict(
    orientation="h",
    yanchor="bottom",
    xanchor="left",
    y=0.99
))



#####car_fuel


pg_first_layout = html.Div([dbc.Container([
html.Br(),
    dbc.Row([html.P("სათბური აირების ემისიები საქართველოში (მეგატონა)", style={ "text-align": "left", 'font-weight': 'bold',  "font-size": "18px", 'font-family': 'Akademiuri'})]),
html.Br(),
    dbc.Row([

        dbc.Col(dbc.Row(
            html.Div([
            dcc.Graph(id="emmision_graph",figure=figm), html.Div([ html.P("წყარო: საქართველოს სტატისტიკის ეროვნული სამსახური")], style={"font-size": "13px", 'font-family': 'Akademiuri'}),] ) ,
       )),

        dbc.Col(html.Div(children =[
html.Div(children = [
html.Div(children =[ dbc.Row([
        dbc.Col(
html.Img(src='data:image/png;base64,{}'.format(encoded_image_car), style={"height":"150px", 'marginLeft':'0px', "margin-right": "500px"}), width=3),
dbc.Col(
html.P("2017 წელს, 1990 წელთან შედარებით, ემისია 21.9 მეგატონით შემცირდა", style={ "text-align": "left", 'font-weight': 'bold',  "font-size": "18px", 'font-family': 'Akademiuri', "margin-top": "40px"}),  width=9
        ),]),]),
    html.P(
           'კლიმატის ცვლილებას სათბურის აირების გაფრქვევა (ემისიები) იწვევს. ძირითადი სათბურის აირებია: წყლის ორთქლი, ნახშირორჟანგი და ოზონი.',
        style={"color":"black", "font-size": "18px", 'text-align': 'left'}),
    html.P(
        '2012-2017 წლებში მნიშვნელოვნადაა გაზრდილი როგორც სათბური აირების ჯამური, ასევე ტრანსპორტის სექტორიდან სათბური გაზების ემისიების მაჩვენებელი.',
        style={"color": "black", "font-size": "18px", 'text-align': 'left'}),


],style={'font-family': 'Akademiuri', "border": "3px solid rgba(28,110,164,0.7)",
                   "border-radius": "9px 9px 9px 9px",  "height":380,  "float": "right", "margin-top":"20" , 'textAlign': 'center', "padding": "30px"}),

        ],)
        ),
    ],  style={"margin-top": "0px"}),
html.Br(),
html.Br(),

    dbc.Row([html.P("2020 წელს სატრანსპორტო სექტორის განაწილება საწვავის ტიპის მიხედვით (ტერაჯოული)",
                    style={"text-align": "left", 'font-weight': 'bold', "font-size": "18px",
                           'font-family': 'Akademiuri'})]),
    dbc.Row([

        dbc.Col( dbc.Row([html.Div(children=[dcc.Graph(id="emmision_graph3",figure=figs), html.Div([ html.P("წყარო: AskGov.ge ")], style={"font-size": "13px", 'font-family': 'Akademiuri'}),] ),] ),width=8),
dbc.Col(
html.Img(src='data:image/png;base64,{}'.format(encoded_image_fuel), style={"height":"100px", "margin-top": "100px"}), width=2),
        dbc.Col(
html.P("საგზაო ტრანსპორტის ძირითადი ნაწილი ნავთობ პროდუქტებს მოიხამრს.", style={ "margin-top": "100px","text-align": "left", 'font-weight': 'bold',  "font-size": "18px", 'font-family': 'Akademiuri'})
        )
    ]),
    html.Br(),
dbc.Row([html.P("2020 წელს, 2011 წელთან შედარებით, 84%-ითაა გაზრდილი ავტომობილების საერთო რაოდენობა, ავტომობილებში უდიდეს წილს კვლავ მსუბუქი ავტომობილები შეადგენს.",
                                                                             style={'font-family': 'Akademiuri', "font-size": "18px", "border": "3px solid rgba(28,110,164,0.7)", "border-radius": "9px 9px 9px 9px", 'textAlign': 'center' })]),
html.Br(),
    dbc.Row([dbc.Col(html.P( "რეგისტრირებული ავტომობილების რაოდენობა", style={ "text-align": "left", 'font-weight': 'bold',  "font-size": "18px", 'font-family': 'Akademiuri'})),
                       dbc.Col(html.P("რეგისტრირებული ავტომებილების ასაკობრივი განაწილება (ათასი ერთეული)",
                     style={"text-right": "center", 'font-weight': 'bold', "font-size": "18px",
                            'font-family': 'Akademiuri'})), ]),
    dbc.Row([
        dbc.Col(dbc.Row([html.Div([dcc.Graph(id="emmision_graph4",figure=fign, style = {'display': 'inline-block'}),
                                   html.Div([ html.P("წყარო: საქართველოს სტატისტიკის ეროვნული სამსახური")], style={"font-size": "13px", 'font-family': 'Akademiuri'})]),
                         ]), width=5),

dbc.Col(dbc.Row([html.Div([dcc.Graph(id="emmision_graph2",figure=figg, style = {'display': 'inline-block'}),
                                   html.Div([ html.P("          წყარო: საქართველოს სტატისტიკის ეროვნული სამსახური")], style={"font-size": "13px", 'font-family': 'Akademiuri'})]),
                         ]), width=5)

    ]),
    html.Br(),
dbc.Row([  html.P("2021 წელს, ელექტრომობილებისა და ჰიბრიდი ავტომობილების წილი ავტოპარკში 0.2% და 6.8%-ს შეადგენს.",
                  style={'font-family': 'Akademiuri', "font-size": "20px", "border": "3px solid rgba(28,110,164,0.7)",
                         "border-radius": "9px 9px 9px 9px", 'textAlign': 'center'}
                  )]),
    html.Br(),
    html.Div([html.P("რეგისტრირებული ავტომებილების საწვავის ტიპის მიხედვით განაწილება (ათასი ერთეული)",
                     style={"text-align": "center", 'font-weight': 'bold', "font-size": "18px",
                            'font-family': 'Akademiuri'})]),


dbc.Row([
dbc.Col(html.Div([
            dcc.Dropdown(id='year_names',
                         options=[{'label': '2021', 'value': '2021 წელი'},
                                  {'label': '2020', 'value': '2020 წელი'},
                                  {'label': '2019', 'value': '2019 წელი'},
                                  {'label': '2018', 'value': '2018 წელი'},
                                  {'label': '2017', 'value': '2017 წელი'}],
                         value='2021 წელი',
                         clearable=False,
                         multi=False,
                         style={"width": "50%", 'float': '4px'}
                         ), html.Div([dcc.Graph(id='car_fuel_type')]),
    ]), ),
html.Div([ html.P("წყარო: საქართველოს სტატისტიკის ეროვნული სამსახური")], style={"font-size": "13px", 'font-family': 'Akademiuri'})
    ]),
], fluid=True)
])


image_filename = 'goal.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')
image_filename_second = '17-goals.png'
encoded_image_second = base64.b64encode(open(image_filename_second, 'rb').read()).decode('ascii')
pg_second_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([html.P("2017 წელს, პარიზის შეთანხმების დამტკიცების შედეგად, საქართველო შეუერთდა შეთანხმების მონაწილე  191 ქვეყანას და განაცხადა მზაობა, "
                                 "რომ პარიზის შეთანხმების მიზნის მისაღწევად საკუთარ წვლილს შეიტანდა, გლობალური საშუალო ტემპერატურის ზრდის წინაინდუსტრიულ დონესთან შედარებით მაქსიმუმ 2°C-მდე, საუკეთესო შემთხვევაში, 1.5°C-მდე შეზღუდვაში."),
            html.P('სტრატეგიის მიხედვით 2030 წლისთვის (2021 წლის ეროვნულ დონეზე განსაზღვრული წვლილის განახლებული დოკუმენტის მიხედვით), 1990 წლის მაჩვენებელთან შედარებით, სათბურის აირების ემისიის 35%-თ შემცირება.'
    ), ],
style={'font-family': 'Akademiuri', "font-size": "18px", "border": "3px solid rgba(28,110,164,0.7)", "border-radius": "9px 9px 9px 9px", "height": 200, "float": "right", "margin-top": "0px",
                      "padding": "10px",  'textAlign': 'left'}),)
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={"height":"100px", 'marginLeft':'100px', 'margin-top':'10px',  "padding":"10 px"}),  width=3),
        dbc.Col(html.H5('მიზანი 2 - 2030 წლისთვის, საბაზისო სცენარით გათვალისწინებულ პროგნოზებთან შედარებით, ტრანსპორტის სექტორში, სათბურის აირების ემისიების 15%-თ შემცირება.', style={"font-size": "18px",'font-family': 'Akademiuri', "padding":"60 px", 'margin-top':'40px'}))
    ]),
html.Br(),
    dbc.Row([
        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image_second), style={"height":"80px", 'marginLeft':'620px' }),),
        dbc.Col(html.Div(children = [
    html.P('კავშირი მდგრადი განვითარების მიზნებთან', style={ "text-align": "center", 'margin-top':'0px', "font-size": "18px"}),
    html.P("3 8 11", style={"color":"green",  "text-align": "center", 'margin-top':'0px', "font-size": "18px", 'font-weight': 'bold' })
],style={'font-family': 'Akademiuri'})
                     )]),
    html.Br(),
    html.Br(),
    html.Div([html.P("საქართველოს კლიმატის ცვლილების 2030 წლის სტრატეგიით განსაზღვრული ამოცანები და ინდიკატორები", style={ "text-align": "center", 'font-weight': 'bold',  "font-size": "18px", 'font-family': 'Akademiuri'})]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.CardBody("2.1 ტრანსპორტის სექტორიდან სათბურის აირების ემისიების რაოდენობა (გგ CO2. ეკვ.)", style={'font-family': 'Akademiuri','background-color': '#607EAA', "height": "18 rem", "border-radius": "9px 9px 9px 9px"}),),
        dbc.Col(dbc.CardBody("2.2 წიაღისეულ საწვავზე მოთხოვნის შემცირებისა და ბიოსაწვავის გამოყენების წახალისება", style={'font-family': 'Akademiuri', 'background-color': '#f9f55c', "height": "16 rem", "border-radius": "9px 9px 9px 9px"}),),
        dbc.Col(dbc.CardBody("2.3 მობილობის არამოტორიზებული საშუალებებისა და საზოგადოებრივი ტრანსპორტის წახალისება", style={'font-family': 'Akademiuri', 'background-color':'#a6bed3', "height": "16 rem", "border-radius": "9px 9px 9px 9px"}),),
        dbc.Col(dbc.CardBody("2.4 ტრანსპორტის სექტორში მტკიცებულებებზე დაფუძნებული ინოვაციური ინიციატივების განხორციელება", style={'font-family': 'Akademiuri', 'background-color':'#c3bad7', "height": "16 rem", "border-radius": "9px 9px 9px 9px"}),)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([ dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph',   children=[
            dcc.Tab(label='2.1.1', style= {'font-family': 'Akademiuri', 'background-color': '#607EAA', 'justify-content': 'center'}, className='custom-tab', value='tab-1-example-graph'),
            dcc.Tab(label='2.1.2', style= {'font-family': 'Akademiuri','background-color': '#607EAA', 'justify-content': 'center'}, className='custom-tab', value='tab-2-example-graph'),
            dcc.Tab(label='2.1.3', style= {'font-family': 'Akademiuri','background-color': '#607EAA','justify-content': 'center'}, className='custom-tab', value='tab-3-example-graph'),
            dcc.Tab(label='2.2.1', style= {'font-family': 'Akademiuri', 'background-color': '#f9f55c','justify-content': 'center'}, className='custom-tab', value='tab-4-example-graph'),
            dcc.Tab(label='2.3.1', style= {'font-family': 'Akademiuri', 'background-color': '#a6bed3','justify-content': 'center'}, className='custom-tab', value='tab-5-example-graph'),
            dcc.Tab(label='2.3.2', style= {'font-family': 'Akademiuri', 'background-color': '#a6bed3','justify-content': 'center'}, className='custom-tab', value='tab-6-example-graph'),
            dcc.Tab(label='2.4.1', style= {'font-family': 'Akademiuri', 'background-color': '#c3bad7','justify-content': 'center'}, className='custom-tab', value='tab-7-example-graph')
            ])
    ]),
    html.Div(id='tabs-content-example-graph'),

        ]), html.Div([ html.P("წყარო: საქართველოს კლიმატის ცვლილების 2030 წლის სტრატეგიის 2021-2023 წლების სამოქმედო გეგმა / "
                              "საქართველოს კლიმატის ცვლილების 2030 წლის სტრატეგიის 2021–2023 წლების სამოქმედო გეგმის 2021 "
                              "წლის განხორციელების ანგარიში (MEPA)")], style={"font-size": "13px", 'font-family': 'Akademiuri'})
], fluid=True)


###map

####


#@app.callback(
 #   Output("page-content", "children"),
  #  [Input("url", "pathname")]
#)
#def render_page_content(pathname):
 #   if pathname == "/page-1":
  #      return [ pg_first_layout
    #    ]
   # elif pathname == "/page-2":
    #    return [ pg_second_layout

  #      ]

source_layout= dbc.Container(html.Div([
    html.H5("გამოყენებული ლიტერატურა:"),
    html.A("1.1  გარემოს სტატისტიკა - გარემოსდაცვითი ინდიკატორები - B-3. სათბური გაზების ემისიები/H-3."
           " საავტომობილო პარკი კატეგორიების მიხედვით/H-4. საავტომობილო პარკი ასაკის მიხედვით (geostat.ge)", href="https://www.geostat.ge/ka/modules/categories/565/garemosdatsviti-indikatorebi"),
    html.Br(),
html.A("1.2	პუბლიკაციები - წლიური- საქართველოს სტატისტიკური წელიწდეული 2021 - თავი 15 (geostat.ge)", href="https://www.geostat.ge/ka/single-categories/95/sakartvelos-statistikuri-tselitsdeuli"),
html.Br(),
html.A("2.  დიზელის მოხმარების სტატისტიკა (AskGov.ge )", href="https://askgov.ge/ka/request/dizelis_moxmarebis_statistika "),
html.Br(),
html.A("3.	საქართველოს ეროვნულ დონეზე განსაზღვრული წვლილი (NDC) (MEPA)", href="https://www.climatebasics.info/_files/ugd/8cfda1_83096a30a509436b871987a0a6f63d07.pdf"),
html.Br(),
html.A("4.	საქართველოს კლიმატის ცვლილების 2030 წლის სტრატეგია და სამოქმედო გეგმა (CSAP) (MEPA)", href="https://www.climatebasics.info/_files/ugd/8cfda1_2ca70f44524c4f29be04bec99f1332c5.pdf "),
html.Br(),
html.A("5.	კლიმატის სამოქმედო გეგმა 2023 (CAP) (MEPA)", href="https://www.climatebasics.info/_files/ugd/8cfda1_7795ff1c6e4e4af08292c19d1b4c16f8.pdf"),
html.Br(),
html.A("6.	საქართველოს კლიმატის ცვლილების 2030 წლის სტრატეგიის 2021–2023 წლების სამოქმედო გეგმის 2021 წლის განხორციელების ანგარიში (MEPA)", href="https://mepa.gov.ge/Ge/Files/ViewFile/52702"),
html.Br(),
html.A("7.	საქართველოს მეოთხე ეროვნული შეტყობინება კლიმატის ცვლილების შესახებ გაეროს ჩარჩო კონვენციისადმი (UNFCCC) (MEPA)", href="https://www.climatebasics.info/_files/ugd/8cfda1_54fef272b72e4edcb86e14d4b51867fe.pdf"),
html.Br(),
html.A("8.	International Energy Agency (IEA) – Transport Improving the sustainability of passenger and freight transport", href="https://www.iea.org/topics/transport?fbclid=IwAR2lz9gy1si9Y3H5ZPUP4Kz5ATPHqT4gwbWh6nuDEOVaZec3883K60tEoI"),
html.Br(),
html.A("9.	Partnership On Sustainable Law Carbon Transport (SLOCAT) –SLOCAT Transport and Climate Change Global Status Report", href="https://tcc-gsr.com/wp-content/uploads/2021/06/Slocat-Global-Status-Report-2nd-edition_high-res.pdf"),
html.Br(),
html.A("10.1 	CO2 emissions (kt)(WB) ", href="https://data.worldbank.org/indicator/EN.ATM.CO2E.KT"),
html.Br(),
html.A("10.2	CO2 emissions from transport (% of total fuel combustion)(WB) ", href="https://data.worldbank.org/indicator/EN.CO2.TRAN.ZS"),
], style= {'font-family': 'Akademiuri'}))

app.layout = html.Div([
dbc.CardHeader("სატრანსპორტო სექტორი და მისი გავლენა კლიმატის ცვლილებაზე", style= {'font-family': 'Akademiuri', "background-color" : "#a0b2cc", "height":"100px", "font-size": "35px", "padding-top": "25px"}),
    dbc.Container([top_line]),
dbc.Container([pg_first_layout]),
dbc.Container(html.Div([middle_line,
html.Br(),
dbc.Container([pg_second_layout]),
    html.Br(),
source_layout
    #dcc.Location(id="url"),
    #sidebar,
    #content,
              ]))
])




@app.callback(
    Output('tabs-content-example-graph', 'children'),
    Input('tabs-example-graph', 'value')
)

def startegy(tab):
    if tab == 'tab-1-example-graph':
        figs1= px.bar(df_strategy, x="წელი", y="ელექტრომობილების წილი საქართველოში რეგისტრირებულ ავტოპარკში", text= "პირველი", color_discrete_sequence=["#d0d9e5"])
        figs1.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title="ელექტრომობილების წილი საქართველოში რეგისტრირებულ ავტოპარკში"
        )
        figs1.update_layout(template="simple_white")
        figs1.update_traces(width=1, textposition='outside')
        return html.Div([
        dcc.Graph(figure = figs1)])
    elif tab == 'tab-2-example-graph':
        figs2= px.bar(df_strategy, x="წელი", y="ჰიბრიდული ავტომობილების წილი საქართველოში რეგისტრირებულ ავტოპარკში", text= "მეორე", color_discrete_sequence=["#d0d9e5"] )
        figs2.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title="ჰიბრიდული ავტომობილების წილი საქართველოში რეგისტრირებულ ავტოპარკში",
        )
        figs2.update_layout(template="simple_white")
        figs2.update_traces(width=1, textposition='outside')
        return html.Div([
        dcc.Graph(figure = figs2)])
    elif tab == 'tab-3-example-graph':
        figs3 = px.bar(df_strategy, x="წელი", y="პირველად ტექნიკურ ინსპექტირებაზე დახარვეზებული ავტომობილების პროცენტული წილი", text='მესამე', color_discrete_sequence=["#d0d9e5"])
        figs3.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title="პირველად ტექნიკურ ინსპექტირებაზე დახარვეზებული ავტომობილების პროცენტული წილი",
        )
        figs3.update_layout(template="simple_white")
        figs3.update_traces(width=1, textposition='outside')
        return html.Div([
        dcc.Graph(figure = figs3)])
    elif tab == 'tab-4-example-graph':
        figs4 = px.bar(df_strategy, x="წელი", y="საქართველოს ტერიტორიაზე ენერგიის საბოლოო მოხმარებაში ყველა სახეობის", text='მეოთხე', color_discrete_sequence=["#d0d9e5"])
        figs4.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title= 'საქართველოს ტერიტორიაზე ენერგიის საბოლოო მოხმარებაში ყველა სახეობის',
        )
        figs4.update_layout(template="simple_white")
        figs4.update_traces(width=1, textposition='outside')
        return html.Div([
            dcc.Graph(figure = figs4)])
    elif tab == 'tab-5-example-graph':
        figs5 = px.bar(df_strategy, x="წელი_2021_გამოტივებით",
                       y="თბილისში მგზავრობის პროცენტული წილი, რომელიც არამოტორიზებული ტრანსპორტით", text='მეხუთე',color_discrete_sequence=["#d0d9e5"])
        figs5.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title= 'თბილისში მგზავრობის პროცენტული წილი, რომელიც არამოტორიზებული ტრანსპორტით (ველოსიპედი და ფეხით სიარული) ხორციელდება',
        )
        figs5.update_layout(template="simple_white")
        figs5.update_traces(width=1, textposition='outside')
        return html.Div([
            dcc.Graph(figure=figs5)])
    elif tab == 'tab-6-example-graph':
        figs6 = px.bar(df_strategy, x="წელი_2021_გამოტივებით",
                       y="თბილისში მგზავრობის პროცენტული წილი, რომელიც საზოგადოებრივი ტრანსპორტი (მეტრო, ავტობუსი, მიკროავტობუსი) ტრანსპორტით ხორციელდება", text='მეექვსე', color_discrete_sequence=["#d0d9e5"])
        figs6.update_layout(
            xaxis_title="თარიღი", yaxis_title="პროცენტული წილი", title= 'თბილისში მგზავრობის პროცენტული წილი, რომელიც საზოგადოებრივი ტრანსპორტით (მეტრო, ავტობუსი, მიკროავტობუსი) ხორციელდება'
        )
        figs6.update_layout(template="simple_white")
        figs6.update_traces(width=1, textposition='outside')
        return html.Div([
            dcc.Graph(figure=figs6)])
    elif tab == 'tab-7-example-graph':
        figs7 = px.bar(df_strategy, x="წელი",
                       y="ტრანსპორტის სექტორში სათბურის აირების ემისიების შემცირების მტკიცებულებებზე დაფუძნებული დამატებითი ინიციატივების რაოდენობა", text='მეშვიდე', color_discrete_sequence=["#d0d9e5"])
        figs7.update_layout(
            xaxis_title="თარიღი", yaxis_title="რაოდენობა", title= 'ტრანსპორტის სექტორში სათბურის აირების ემისიების შემცირების მტკიცებულებებზე დაფუძნებული დამატებითი ინიციატივების<br> რაოდენობა'
        )
        figs7.update_layout(template="simple_white")
        figs7.update_traces(width=1, textposition='outside')
        return html.Div([
            dcc.Graph(figure=figs7)])


@app.callback(
    Output("car_fuel_type", "figure"),
    Input('year_names', 'value'))
def car_fuel (year_names):

        fig=px.pie(data_frame=df_auto_park_fuel, values=year_names, names='ავტომობილები საწვავის ტიპის მიხედვით', hole=.5, color_discrete_sequence=px.colors.sequential.dense)
        fig.update_traces(textposition='inside', showlegend= True)
        fig.update_layout(legend_font_size= 10)
        fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)