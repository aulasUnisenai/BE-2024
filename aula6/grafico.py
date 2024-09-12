# Rota para visualizar o dashboard
@app.route('/dashboard')
def dashboard():
    # Consultando os dados do banco
    dados = DadosSensor.query.order_by(DadosSensor.timestamp.asc()).all()

    # Preparando os dados para os gráficos
    timestamps = [d.timestamp.strftime('%d/%m/%Y %H:%M:%S') for d in dados]
    temperaturas = [d.temperatura for d in dados]
    umidades = [d.umidade for d in dados]

    # Gráfico combinado de Temperatura e Umidade
    fig = go.Figure()

    # Linha de Temperatura
    fig.add_trace(go.Scatter(
        x=timestamps, 
        y=temperaturas, 
        mode='lines+markers', 
        name='Temperatura (°C)', 
        line=dict(color='#FF6347'),
        marker=dict(size=6),
        hovertemplate='Data: %{x}<br>Temperatura: %{y}°C<extra></extra>'
    ))

    # Linha de Umidade
    fig.add_trace(go.Scatter(
        x=timestamps, 
        y=umidades, 
        mode='lines+markers', 
        name='Umidade (%)', 
        line=dict(color='#4682B4'),
        marker=dict(size=6),
        hovertemplate='Data: %{x}<br>Umidade: %{y}%<extra></extra>'
    ))

    # Layout do gráfico
    fig.update_layout(
        title_text='Temperatura e Umidade ao Longo do Tempo',
        xaxis_title='Data e Hora',
        yaxis_title='Medições',
        legend=dict(
            x=1,  
            y=0.5,  
            font=dict(size=10),
            bgcolor="rgba(255, 255, 255, 0.5)"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            tickangle=-45,  
            zeroline=False,
            nticks=10  
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=30, r=100, t=30, b=30),  
        hovermode="x"
    )

    # Converter o gráfico para HTML
    combined_graph = pio.to_html(fig, full_html=False)

    # Renderizar o template com o gráfico
    return render_template('dashboard.html', combined_graph=combined_graph)