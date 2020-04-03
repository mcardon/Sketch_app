# -*- coding: utf-8 -*-
# Created by Melissa Cardon

import sys
import os
import json
import datetime
import deviantart
#from Deviantart_sketch_functions import DA_sketch_appli

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# ---------------- READ CONFIG -------------------
if os.path.exists("/var/www/Sketch_app/"):
    # if on tiphaine's server
    configfile = "/var/www/Sketch_app/config_server.json"
else:
    # else, i.e. local development
    configfile = "./config.json"

config = json.load(open(configfile))

# ------------------ COLORS -----------------------

# color_2 = '#BBBBBB'
color_head = '#AAAADD'
color_left = '#AAAADD'
color_right = '#FFFFFF'
color_img_div = '#FFFFFF'

with open(config["credential_path"], "r") as read_file:
	da_logs = json.load(read_file)
# ------------------ DEBUG PARAMS -----------------
RUN_DA = True
run_app = True
# ------------------ DA API -----------------------




# ------------------ DASH APP -----------------------
dropdownmenu = dcc.Dropdown(
	id='folders-dropdown',
	options=[
		{'label': 'Loading, please wait...', 'value': '0'}
	],
	value='0'
)

# App
app = dash.Dash()
server = app.server
app.css.append_css({
	'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
# assigning callbacks to components
# that are generated by other callbacks
# (and therefore not in the initial layout), then
# you can suppress this exception by setting
app.config['suppress_callback_exceptions']=True

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
img_url_test = ['https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/2831f606-837e-4d80-9506-6c57243f6d31/dd9bbkc-b7b1a125-06b6-44ef-a868-47fd5f26ea02.jpg',
'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/70834e96-067e-42b9-8c26-8fe104d3fbaa/dd9bbn2-fd35a3c4-f95a-47ba-9253-8bbee53e1b73.jpg/v1/fill/w_900,h_1125,q_75,strp/zelda___botw2_by_larienne_dd9bbn2-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTEyNSIsInBhdGgiOiJcL2ZcLzcwODM0ZTk2LTA2N2UtNDJiOS04YzI2LThmZTEwNGQzZmJhYVwvZGQ5YmJuMi1mZDM1YTNjNC1mOTVhLTQ3YmEtOTI1My04YmJlZTUzZTFiNzMuanBnIiwid2lkdGgiOiI8PTkwMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.O0OG8lr3TlphoQfOAzCqMKcf87VSqIoSDru0cWGCAU0']
# Layout
app.layout = html.Div(
	[
                html.Link(
                            rel='stylesheet',
                                    href='https://codepen.io/chriddyp/pen/bWLwgP.css'
                        ),
		html.Div(
			[
				html.Div(
					[html.H1('Sketchtember_debugphase2', id='title', n_clicks=0)], 
					style={'background': color_head},
					className="twelve columns"),
			], 
		className="row"
		),
		html.Div(
			[
				html.Div(
					[dropdownmenu], 
					style={'background': color_head},
					className="two columns"),
			], 
		className="row"
		),
		html.Div(
			[
				html.Div(
					[
						dcc.RadioItems(
							id='radio_timing',
							options=[
								{'label': 'Just looking (10 images in 30 sec)', 'value': '3,6,9,12,15,18,21,24,30,33'},
								{'label': 'Warm up (12 min, 10 sketches, increasing time)', 'value': '30,60,90,120,150,180,240,300,420,720'}
								#{'label': 'Workout (30 min, 6 sketches of 5 min)', 'value': '300,600,900,1200,1500,1800'}
							],
							value='30,60,90,120,150,180,240,300,420,720',
							labelStyle={'display': 'inline-block'}
						),
						html.Button(
							'Start', 
							value='value button',
							n_clicks=0,
							id='button_start'),
						html.Div(id='master_clock_box'),
						html.Div(id='da-api-results-box', 
							style={'display': 'none'})
					], 
					style={'background': color_left},
					id='div_buttons_timer',
					className="two columns"),
				html.Div(
					['Click Start to begin warmup sketch session'],
					style={
					'background': color_img_div},
					id='img_display',
					className="eight columns"),
				html.Div([''],
					style={'background': color_right,
					'font-size': '40px'},
					id='timer_display',
					className="two columns")
			], 
		className="row"
		),
	])

# ------------------ FUNCTIONS -----------------------
def fetch_folders(username='Sketchtember'):
	da = deviantart.Api(da_logs["id"], da_logs["mdp"])
	LIMIT = 15
	has_more = True
	offset = 0
	all_folders = []
	while(has_more):
		collec = da.get_collections(username=username, offset=offset, limit=LIMIT)
		folder = collec['results']
		all_folders += folder
		has_more = collec["has_more"]
		offset += LIMIT
	return all_folders

def choose_img_display(img_url, img_height, img_width, max_height):
	ratio_img = max_height/img_height
	# choose the display depending on img ratio
	if img_height>= img_width:
		# print('width:', str(int(img_width*ratio_img))+'px')
		# print('width:', str(int(ratio_img*100))+'%')
		img_display = html.Img(
			src=img_url,
			style={
				# 'width': str(int(ratio_img*100))+'%'
				'width': '100%'
			})
		return img_display
	else:
		img_display = html.Img(
			src=img_url,
			style={
				'width': '100%'
			})
		return img_display

def fetch_img(n_img, folderid, username):
	# max number of img : 50
	if RUN_DA & (n_img <= 50):
		print('Fetching img from Deviantart')
		#create an API object with your client credentials
		da = deviantart.Api(da_logs["id"], da_logs["mdp"])
		#sketchit = DA_sketch_appli(da)
		#folderid = 'DC11C610-7878-FCF8-CDDF-DB9428F7CB29' # Sketch folder
		#folderid='5B222A0F-8E0B-D602-920C-BCA299BEAE3E'#amphibians
		#folderid = '0BB1B33D-87F6-F45A-ACB9-3AE61EA78C76' # inspiration 2017
		#folderid = '93C80B8C-18E8-98CC-764E-7CC2258ED2CD' # Birds
		#folderid =  "F4E960A3-2D38-9731-D51E-878957299FC5" # Sculptures
		#folderid="AA53736E-41A2-7032-C280-F39B57ED6E7D"#pantyhose-fan
		#folderid="44A4EDFE-8A95-06B8-2B48-DF5D873DA65E"#parazelsus


		infos_devs = []
		#collec = da.get_collection(folderid, username='l-Zoopy-l', offset=10, limit=10)
		collec = da.get_collection(folderid, username=username, offset=0, limit=12)

		#
		imgs = collec['results']
		urls = [imgs[i].preview['src'] for i in range(len(imgs))]
		dims = [[imgs[i].preview['width'], imgs[i].preview['height']] for i in range(len(imgs))]
		
		print('api query completed')
	else:
		urls = ['https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/2831f606-837e-4d80-9506-6c57243f6d31/dd9bbkc-b7b1a125-06b6-44ef-a868-47fd5f26ea02.jpg',
		'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/70834e96-067e-42b9-8c26-8fe104d3fbaa/dd9bbn2-fd35a3c4-f95a-47ba-9253-8bbee53e1b73.jpg/v1/fill/w_900,h_1125,q_75,strp/zelda___botw2_by_larienne_dd9bbn2-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTEyNSIsInBhdGgiOiJcL2ZcLzcwODM0ZTk2LTA2N2UtNDJiOS04YzI2LThmZTEwNGQzZmJhYVwvZGQ5YmJuMi1mZDM1YTNjNC1mOTVhLTQ3YmEtOTI1My04YmJlZTUzZTFiNzMuanBnIiwid2lkdGgiOiI8PTkwMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.O0OG8lr3TlphoQfOAzCqMKcf87VSqIoSDru0cWGCAU0']
		dims = [[3000,1300], [3000,1300]]

	return {'urls': urls, 'dims': dims}


# ------------------ CALLBACKS -----------------------
@app.callback(
	Output("folders-dropdown", "options"),
	[Input("title", "value")],
)
def update_dropdown(value): 
	all_folders = fetch_folders('Sketchtember')
	options = []
	for i in range(0, len(all_folders)):
		if (all_folders[i]['name']=='Featured') | (all_folders[i]['name'][0]!='2') :
			continue
		options.append(
			{"label": all_folders[i]['name'], "value": all_folders[i]['folderid']}
		)
	return options



# when the button is clicked, it creates a master clock
@app.callback(
	[Output('da-api-results-box', 'children'),
	Output('master_clock_box', 'children')],
	[Input('button_start', 'n_clicks')],
	[State('radio_timing', 'value'),
	State('folders-dropdown', 'value')]
	)
def create_master_clock(n_clicks, radio_value, dropdown_value):
	if n_clicks > 0:
		master_clock = dcc.Interval(
			id='master_clock',
			interval=1*1000, # in milliseconds
			n_intervals=0
		)
		# fetch deviations with Deviantart API
		n_img = len(radio_value.split(','))
		img_dict = fetch_img(n_img, dropdown_value, 'Sketchtember')
	else:
		print('sending dummy json result to da-api-results-box')
		master_clock = ['']
		img_dict = {'urls': [], 'dims': []}
	# output the results of the api first
	# because master clock needs it as soon as it is created
	# do not change order this was a tricky one.
	return json.dumps(img_dict), master_clock


#master clock will fire the display of images
@app.callback([
	Output('img_display', 'children'),
	Output('timer_display', 'children')
	],
	[Input('master_clock', 'n_intervals')],
	[State(component_id='radio_timing', component_property='value'),
	State('da-api-results-box', 'children')])
def fire_img_timer(n_intervals, radio_value, json_dev):
	img_dict_one = json.loads(json_dev)

	# double img list (in case some are missing)
	img_dict = {k:img_dict_one[k]*2 for k in img_dict_one.keys()}
	#print('This is img dict')
	#print(img_dict)
	# display imgs at the right time
	#session_time = [30,60,90,120,150,180,240,300,420,720]
	#session_time = [5,10,15,20,25,30,35,40,45,50]
	session_time = [int(t) for t in radio_value.split(',')]
	i=0
	while n_intervals > session_time[i]:
		i = i +1
		#print('increment')
		if i == len(session_time):
			break

	if i < len(session_time):
		print(n_intervals, session_time[i],i)
		img_url = img_dict['urls'][i]
		max_height = 500
		img_width = img_dict['dims'][i][0]
		img_height = img_dict['dims'][i][1]
		img_display = choose_img_display(img_url, img_height, img_width, max_height)
	else:
		img_display = html.Div(['Félicitations !!! (et merciiiiiii)'])
	timer_display = str(session_time[min(len(session_time)-1,i)] - n_intervals)
	return img_display, timer_display


if (__name__ == '__main__') & run_app:
	app.run_server(host="0.0.0.0", debug=True)
