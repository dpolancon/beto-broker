# Resumen Ejecutivo

Desarrollar un *sistema de trading algorítmico de muy corto plazo* basado en ML supervisado y señales de sentimiento social requiere **varios pilares clave**: fuentes de datos fiables (mercado y redes sociales), indicadores de sentimiento (“espíritus animales”), análisis de influencers en redes, modelos ML calibrados con riesgos acotados, y un monitoreo humano estricto con **kill switch**. La literatura apunta a que los enfoques híbridos –que combinan análisis técnico y de sentimiento– son más prometedores【23†L43-L47】【21†L333-L341】. Por ejemplo, modelos que integran texto y precios son candidatos fuertes para una estrategia generalizada【23†L43-L47】. Twitter (ahora X) es una fuente de datos ampliamente usada para medir “la temperatura del mercado” en tiempo real【14†L588-L597】【16†L58-L64】. Indicadores de sentimiento pueden extraerse mediante NLP de tuits, y al cruzarlos con análisis de redes sociales podemos detectar patrones de **manada** e influencias de *finfluencers*. Todo esto nutre un modelo ML supervisado que emita señales de trading. Es esencial implementar límites de riesgo (posicionales, stop-loss) y un kill switch automático que apague el algoritmo ante anomalías【21†L333-L341】. A continuación se detallan estos componentes de diseño estratégico.

## 1. Fuentes de datos y extracción en tiempo real

**Mercado de capitales**: Se parte de datos clásicos de trading (cotizaciones de acciones, futuros, pares de divisas, índices) con frecuencia intradía (1m, tick). Esta data proviene de feeds oficiales de bolsas o brokers (por ejemplo, IBKR, Saxo), incluyendo precios, volúmenes y profundidad.  

**Redes sociales (X/Twitter)**: Para captar *sentimiento de mercado*, X ofrece APIs (streaming y REST) que permiten recolectar tuits en tiempo real. Bibliotecas como **Tweepy** en Python facilitan la conexión y el *streaming* de mensajes por palabras clave o cuentas específicas【14†L588-L597】. De acuerdo a IBKR, “Twitter… se usa ampliamente como indicador de sentimiento de mercado”【14†L588-L597】. También se pueden complementar con otras fuentes (noticias financieras, foros) pero aquí el foco es X. El scraping en tiempo real (API stream) abastece un motor de NLP.  

**Data enriquecida**: Además de texto, conviene incluir metadatos: hora, ubicación, hashtags, y redes de interacción (retuits, menciones). Esto permite inferir qué *comunidades* discuten determinados activos. La preparación de los datos implica limpieza (eliminar spam/ruido), normalización (stemming, lematización) y tokenización. 

## 2. Indicadores de sentimiento y “espíritus animales”

**Sentimiento de mercado**: Se crean indicadores cuantitativos del ánimo inversor. Por ejemplo, un score de sentimiento (positivas vs negativas) por activo, extraído de tuits relevantes. Según un estudio reciente, “el análisis de sentimientos tiene un enorme potencial como herramienta de forecasting, proporcionando información sobre patrones de mercado y estado de ánimo de inversores”【16†L23-L32】.   Keynes definió los *“espíritus animales”* como las emociones (confianza, miedo, euforia) que impulsan el mercado【12†L252-L261】【12†L302-L310】. En este contexto, identificamos volúmenes atípicos de tuits, subidas repentinas de menciones positivas, o hashtags emergentes que indiquen euforia o pánico. Por ejemplo, un aumento rápido en comentarios optimistas puede prever un movimiento alcista incluso sin noticias económicas sólidas【12†L252-L261】.

**NLP y ML supervisado**: Los tuits se procesan con técnicas de NLP (modelos basados en transformers, BERT/RoBERTa adaptados a finanzas, o clasificación lexicón+ML) para asignar polaridad y relevancia. Se pueden usar herramientas de sentimiento entrenadas en finanzas (por ejemplo, alfabeto «fear/greed»). Con el aporte de ML, mejoras recientes han logrado integrar aprendizaje automático para extraer con mayor precisión el pulso del mercado【16†L23-L32】. Un posible flujo: recolectar tuits con palabras clave del activo → preprocesamiento lingüístico → modelo ML que clasifica sentimiento y temáticas (p.ej., *compra*, *venta*, *subida*, *bajada*)【16†L23-L32】【23†L93-L100】.

**Métricas compuestas**: Para cada activo/sector se puede definir un indicador de *sentimiento neto*, p.ej. razón de tuits positivos vs negativos, o score medio ponderado por influencia del emisor. Otro indicador sería la variación porcentual de menciones (indica euforia). Estas señales se cruzan con datos técnicos (volatilidad, tendencia) para formar señales finales. Estudios muestran que incluir datos de sentimiento en modelos ML mejora la precisión de predicción de la dirección de mercado (no de precio exacto)【4†L308-L310】. 

## 3. Análisis de redes sociales e identificación de influencers

Las emociones de “manada” emergen en redes. Usando **Análisis de Redes Sociales (SNA)** podemos detectar comunidades y figuras influyentes. El trabajo de Ku et al. (2023) propone modelar Twitter como una red dirigida donde se identifican usuarios influyentes y grupos conectados mediante métricas como PageRank【10†L162-L170】【10†L271-L278】. En práctica, construimos un *grafo* donde nodos son usuarios y aristas representan interacciones (retuits, menciones). Herramientas de SNA (NetworkX, Gephi) permiten calcular influencia central: “los influencers son usuarios con muchos seguidores y alto grado de compromiso; difunden mensajes con fuerza en la red”【10†L271-L278】.

**Comunidades y herd**: Al agrupar usuarios por temas (hashtags) y medir la sincronía de sus mensajes, podemos detectar comportamientos gregarios. Por ejemplo, si un pequeño grupo de *finfluencers* empieza a promocionar un activo, la curva de sentimiento general puede dispararse. Una estrategia es monitorear los “centros de masa” en la red: si un influencer clave cambia su tono, puede generar avalanchas de trading (comportamiento de manada). Estudios muestran que en mercados especulativos (memestocks, criptos) las redes sociales dominan las dinámicas de precios【8†L81-L85】: “los inversores de memestocks no operan según fundamentos, sino sensibles a movimientos de manada/sentimiento”【8†L81-L85】.

En resumen, cruzamos el análisis de contenido con SNA: un tweet puede tener más peso si proviene de un influencer financiero en nuestra red. Los indicadores finales incluirían la variación en la actividad de los nodos más influyentes (por ejemplo, cambio en sentimiento promedio de usuarios con PageRank alto) y métricas de densidad de la red (buscando estallidos de comunicaciones).  

## 4. Modelo de trading supervisado y calibración algorítmica

Con las señales de sentimiento y las variables de mercado, entrenamos un modelo ML supervisado que decida entradas/salidas muy corto plazo. Por ejemplo, se pueden usar clasificadores (regresión logística, árboles, redes neuronales) que, dados vectores de features (momento técnico + ánimo social), predigan *dirección de precio intradía*. La literatura indica que la precisión es limitada (p.ej. ~50–70%) y que los enfoques híbridos son mejores【23†L43-L47】【4†L308-L310】.  

**Características (features)**: Las variables típicas incluyen indicadores técnicos (momentum, medias móviles, volumen, volatilidad implícita), más las métricas sociales mencionadas (sentimiento neto, cambios de menciones, actividad de influencers). Cada tic (minuto, 5m, 1h) el algoritmo recopila este vector.  

**Entrenamiento**: El ML supervisado requiere datos etiquetados. Por ejemplo, se puede usar el retorno intradía siguiente (positiva/negativa) como etiqueta de entrenamiento. Se entrena periódicamente usando datos recientes (backtests over historial) para que el modelo “aprenda” la relación entre sentido del mercado y movimiento de precios. Idealmente se reentrena diario/semanal para adaptarse a cambios de régimen. [23] subraya que “los mejores modelos que combinan sentimiento y técnica” son candidatos ideales【23†L43-L47】.

**Calibración y validación**: Se debe calibrar (ajustar hiperparámetros) con métodos cross-validation usando walk-forward validation. Dado el sesgo de look-ahead en high-frequency, conviene validación en bloque temporal. Métricas clave: precisión direccional, Sharpe ratio de la estrategia, drawdown máximo. La investigación apunta a que los datos de sentimiento incrementan el *Sharpe* o aciertos direccionales【4†L308-L310】, pero que el performance sigue siendo moderado.

**Estrategias de señal**:  
- *Entradas* cuando el modelo indica alta probabilidad de movimiento (p.ej., >60% de que suba/baje).  
- *Stop-Loss* y *Take-Profit* basados en rangos de retorno esperados (para acotar pérdidas), configurable según escenario.  
- *Alocación de capital*: dado el alto riesgo, se sugiere diversificar en varias ideas pequeñas (p.ej., no invertir todo en un solo asset, sino en portafolio).  
- El algoritmo puede cubrir posiciones largas con cortas en el mismo sector (pair trades) si detecta señales contrarias.

## 5. Supervisión humana y mecanismos de corte (“kill switch”)

**Control en tiempo real**: El diseño propuesto exige que un supervisor humano monitoree continuamente. Aunque el sistema opere automáticamente, el humano actúa como interruptor final. Debe existir una interfaz de monitoreo de métricas clave (PNL intradía, exposición neta, indicadores de anomalía). Por ejemplo, si el drawdown supera un umbral, se activa alerta.

**Kill switch**: Siguiendo mejores prácticas (FIA 2024)【21†L333-L341】, se implementa un *kill switch* que detiene instantáneamente el trading algorítmico. Según la guía, “un kill switch…deshabilita inmediatamente toda actividad de trading…previniendo nuevas órdenes y cancelando las órdenes en curso”【21†L333-L341】. Este mecanismo debe usarse como último recurso ante errores críticos (ej.: modelo fuera de base, mercado anómalamente volátil, pérdidas inesperadas). 

**Reglas de corte**: Entre triggers posibles:
- **Pérdida límite**: exponer del capital (ej. –5% intradía) activa corte automático.  
- **Desconexión de datos**: fallo en ingesta de datos (mercado o Twitter) suspende trading.  
- **Señales disonantes**: si señales técnicas y sentiment divergen fuertemente, puede indicar data corrupta.  
- **Anomalías de latencia**: atrasos en ejecución obligan a parar.  

Además, la supervisión manual permite reentrenar o ajustar el modelo en caliente si se detecta *drift* (cambio en relación señal-mercado). Mientras el humano vigila, “la estrategia sólo debe funcionar bajo supervisión, de modo que ante una tendencia de pérdida el algoritmo pueda detenerse de inmediato” (requisito del problema).

## 6. Backtesting, stress tests y métricas operativas

Antes de producción se simula con datos históricos y simuladores:
- **Backtest con tweets**: se requiere un historial de tuits (p.ej. archivados) sincronizado con precios. Se recrea la estrategia minuto a minuto, validando retornos.  
- **Simulaciones de shocks**: escenarios de crisis, “flash crash”, o ruptura de mercados (por ej. COVID, eventos geopolíticos) para ver cómo responde el modelo.  
- **Métricas**: coeficientes de Sharpe y Sortino diarios, % de días con ganancia, max drawdown en periodo simulado, precisión de señal. También métricas de la red de influencers: ¿con qué lead time cambia el sentimiento antes del mercado?  

**Indicadores de operatividad**: Por ser muy corto plazo, se controlan latencias (tiempo entre señal y orden), deslizamiento (slippage), y tasa de llenado de órdenes. En portafolio diversificado, se monitorizan varianza entre activos. Por ejemplo, el éxito puede medirse con el gráfico de PNL vs tiempo acumulado, y correlación con indicadores de sentimiento.  

## 7. Consideraciones de riesgo y éticas

Este sistema es *de alto riesgo* por su horizonte ultracorto y dependencia de señales sociales poco ortodoxas. Se debe advertir que incluso con supervisión, las inversiones pueden perder mucho. Hay que cumplir regulaciones (p.ej., no usar información privada, respetar términos de API de X) y manejar la privacidad de datos. Además, dado el enfoque “best effort”, se requiere advertir que los resultados dependen críticamente de la correcta calibración y vigilancia continua. Como dice Investopedia sobre los *“espíritus animales”*, las emociones pueden generar **burbujas o pánicos** que escapan al análisis fundamental【12†L252-L261】【12†L302-L310】. El sistema propone aprovechar estas dinámicas, pero con límites estrictos de pérdida y supervisión activa.

En síntesis, los pilares estratégicos son: (1) alimentación de datos de trading y social media en tiempo real; (2) procesamiento NLP para producir indicadores de ánimo; (3) análisis de redes para identificar comportamientos de manada e influencers claves; (4) un modelo ML entrenado supervisadamente que combine esas señales con técnicas clásicas; y (5) una arquitectura operativa con monitoreo humano y mecanismos de parada inmediata【21†L333-L341】【23†L43-L47】. Con este esqueleto se puede implementar una *estrategia algorítmica* muy corto plazo, diversificada y de alto riesgo, orientada a obtener ganancias diarias mientras el supervisor esté activo. 

**Fuentes:** literatura académica y guías de trading algorítmico recomiendan combinar análisis técnico con sentimiento social【23†L43-L47】【16†L23-L32】. El uso de Twitter/X como fuente de sentimiento es habitual en sistemas de trading cuantitativo【14†L588-L597】【16†L58-L64】. Las prácticas de riesgo insisten en tener un kill switch supervisado para detener algoritmos desbordados【21†L333-L341】, y estudios recientes confirman que las manadas en redes sociales pueden mover el precio (meme stocks) al margen de fundamentos【8†L81-L85】. Estos hallazgos apoyan el enfoque propuesto aquí.