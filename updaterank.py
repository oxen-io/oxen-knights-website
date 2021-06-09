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
    <div class="tbl-header">
        <table cellpadding="0" cellspacing="0" border="0">
            <thead>
    <th class="top-cell"><font class="column_name">Flair</font></th>
    <th class="top-cell"><font class="column_name">Rank</font></th>
    <th class="top-cell"><font class="column_name">Points</font></th>
    <th class="top-cell"><font class="column_name">Reward</font></th>
        </thread>
        </table>
    </div>
    <div class="tbl-content">
        <table cellpadding="0" cellspacing="0" border="0">
            <tbody>
                <tr>
    """
    end_html = "</table></div></body></html>{% endblock %}"
    for index, row in ranking.iterrows():
        if row['REWARD']!=row['REWARD']:
            start_html += f"""<tr>
            <td><img style="width:100px" src ="../{row['IMG']}"></th>
            <td>{row['RANK']}</td>
            <td class="points-text">{row['POINTS']}</td>
            <td>-</td>
            """

        else:
            start_html += f"""<tr>
            <td><img style="width:100px" src ="../{row['IMG']}"></th>
            <td>{row['RANK']}</td>
            <td class="points-text">{row['POINTS']}</td>
            <td>{row['REWARD']}</td>
            """


    start_html += end_html
    f = open('scoreboard/templates/templatesviews/rankingreward.html','w', encoding="utf-8")
    f.write(start_html)
    f.close()

rankings(pd.read_csv('ranking.csv'))