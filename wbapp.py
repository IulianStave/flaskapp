#win: python -m venv virtual
#linux: python -m virtualenv virtual
# and use python and pip from virtual environment folder
# run with `virtual\Scripts\python wbapp.py`
# install missing packages run: flaskapp>virtual\Scripts\pip install bokeh
# virtual\Scripts\python wbapp.py


from flask import Flask, render_template

#instantiate the class
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/plot/')
def plot():
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.models.annotations import Title
    from datetime import datetime as dt
    from bokeh.resources import CDN

    def inc_dec(open, close):
        if open < close:
            return 'Increase'
        elif open > close:
            return 'Decrease'
        else:
            return 'Equal'
    #start_date = dt(2019,10,1)
    #end_date = dt(2019,10,10) 

    start_date = dt(2019,3,1)
    end_date = dt(2019,5,10) 

    hours_12_in_ms = 12*60*60*1000

    df = data.DataReader(name = "GOOG", data_source = "yahoo", start = start_date, end = end_date)
    #print(df)
    # 12 hours width, 12 hours gap, 
    chart  = figure(x_axis_type = 'datetime', width = 1000, height = 300)
    chart.title.text = "Chart stocks"
    #print(df.index) 
    df["Status"] = [inc_dec(open, close) for open, close in zip(df.Open, df.Close)]
    df["Middle"] = (df.Open + df.Close)/2
    df["Height"] = abs(df.Close - df.Open)
    chart.grid.grid_line_alpha = 0.3

    chart.segment(df.index, df.High, df.index, df.Low, color = "Black")
    chart.rect(df.index[df.Status == 'Increase'], df.Middle[df.Status == 'Increase'], hours_12_in_ms, df.Height[df.Status == 'Increase'], fill_color = "#CCFFFF", line_color = "black")

    chart.rect(df.index[df.Status == 'Decrease'], df.Middle[df.Status == 'Decrease'], hours_12_in_ms, df.Height[df.Status == 'Decrease'], fill_color = "#FF3333", line_color = "gray")

    script1js, div1 = components(chart)
    #print(script1js)
    #print(div1)

    cdn_js = CDN.js_files[0]
    #cdn_css = CDN.css_files[0]
    #output_file('stocks.html')
    #show(chart)
        
    #return render_template("plot.html", cdn_js=cdn_js, cdn_css=cdn_css, script1js=script1js, div1=div1)
    return render_template("plot.html", cdn_js=cdn_js, script1js=script1js, div1=div1)

    
@app.route('/about/')
def about():
    return render_template("about.html",say_hi_name="Iulian")

#when the script is executed by running the command 
# 'python wbapp.py' the __name__ variable gets value __main__
if __name__=="__main__":
    app.run(debug=True)