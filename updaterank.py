import pandas as pd

def rankings(ranking):
        
    start_html = """

    {% extends 'base.html' %}

    {% block body %}
 
    <body>

    <div class="container">
    <center>
    <img width="350px" class="pbot20" src="../static/assets/OXEN_BRAND_PRIMARY.png"><br>
    <h1 class="pbot10">Ranking and Rewards</h1></center>
    <table>
    <th class="top-cell"><font class="column_name">Flair</font></th>
    <th class="top-cell"><font class="column_name">Rank</font></th>
    <th class="top-cell"><font class="column_name">Points</font></th>
    <th class="top-cell"><font class="column_name">Reward</font></th>
    """

    end_html = "</table></div></body></html>{% endblock %}"
    for index, row in ranking.iterrows():
        if row['REWARD']!=row['REWARD']:
            start_html += f"""<tr>
            <th class="number"></th>
            <th class="number">{row['RANK']}</th>
            <th class="number">{row['POINTS']}</th>
            <th class="number">\/</th>
            """

        else:
            start_html += f"""<tr>
            <th class="number"></th>
            <th class="number">{row['RANK']}</th>
            <th class="number">{row['POINTS']}</th>
            <th class="number">{row['REWARD']}</th>
            """

        
    start_html += end_html
    f = open('scoreboard/templates/templatesviews/rankingreward.html','w', encoding="utf-8")
    f.write(start_html)
    f.close()

rankings(pd.read_csv('ranking.csv'))