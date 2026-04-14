```mermaid
%%{init: {'theme':'redux', 'look': 'neo'}}%%
graph TB
    %% ==========================================
    %% 🎨 DEFINICIÓN DE CLASES Y ESTILOS (classDef)
    %% ==========================================
    classDef init fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#bf360c,rx:5px,ry:5px
    classDef process fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1,rx:5px,ry:5px
    classDef condition fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17,rx:5px,ry:5px
    classDef loop fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#4a148c,rx:15px,ry:15px
    classDef output fill:#e8f5e9,stroke:#43a047,stroke-width:2px,color:#1b5e20,rx:5px,ry:5px
    classDef empty fill:none,stroke:none,color:#000

    %% ==========================================
    %% 📖 SUBGRAPH: LEYENDA (Referencia visual)
    %% ==========================================
    subgraph LEGEND [📖 Leyenda de Nodos]
        direction LR
        L1([📥 Inputs / Init]):::init
        L2[⚙️ Proceso / Cálculo]:::process
        L3{❓ Condicional}:::condition
        L4((🔁 Bucle For/While)):::loop
        L5[/📊 Output / Métricas/]:::output
    end

    %% Espaciador invisible para organizar el layout
    LEGEND ~~~ SYSTEM_WRAPPER

    %% ==========================================
    %% 🏗️ ESTRUCTURA PRINCIPAL DEL SISTEMA
    %% ==========================================
    subgraph SYSTEM_WRAPPER [ ]
        direction TB
        
        %% --- MÓDULO 1: INPUT E INICIALIZACIÓN ---
        subgraph INIT [📥 Módulo de Inicialización]
            direction TB
            %% Start([🏁 Inicio de Ronda]):::init
            Start((🏁 Inicio de Ronda)):::init
            Pay[💰 Costo Entrada: 35 monedas]:::init
        end

        %% --- MÓDULO 2: MOTOR DE SIMULACIÓN ---
        subgraph SIM [⚙️ Motor de Simulación]
            direction TB
            
            subgraph SEARCH [🔍 Fase de Búsqueda]
                %% GenX[🎲 Generar X ~ Poisson 3]:::process
                %% GenX["🎲 Generar $X\sim Poisson\left(3\right)$"]:::process
                %% GenX["🎲 Generar X​∼Poisson(3)"]:::process
                GenX["🎲 Generar <div style='text-align:center; font-size:18px;'><b>X</b> &sim; Poisson(3)</div>"]:::process
                CheckX{❓ X = 0?}:::condition
            end

            subgraph WEIGH [⚖️ Fase de Pesaje]
                LoopStart((🔁 Para i=1 hasta X)):::loop
                %% GenW[🎲 Generar W_i ~ Exponencial 2]:::process
                %% GenW["🎲 Generar $w_{i} \sim exp(2)$"]:::process
                %% GenW["🎲 Generar w_i​∼exp(2)"]:::process
                GenW["🎲 Generar <div style='text-align:center; font-size:18px;'><b>w<sub>i</sub></b> &sim; Exp(2)</div>"]:::process
                SumW[➕ Sumar a Peso Total]:::process
                LoopEnd((🔁 Siguiente i)):::loop
            end

            subgraph APPRAISE [💎 Fase de Tasación]
                CalcBase[🧮 Recompensa Base = Peso Total * 5]:::process
                %% GenB[🎲 Bono B ~ Bernoulli 0.05]:::process
                GenB["🎲 Bono <div style='text-align:center; font-size:18px;'><b>B</b> &sim; Bernoulli(0.05)</div>"]:::process
                CheckB{❓ B = 1?}:::condition
                RewardDouble[✨ Final = Base * 2]:::process
                RewardNormal[💵 Final = Base]:::process
            end
        end

        %% --- MÓDULO 3: PROCESAMIENTO ESTADÍSTICO ---
        subgraph STATS [📊 Módulo de Resultados]
            direction TB
            CalcNet[📈 Ganancia Neta = Final - 35]:::process
            SaveResult[/💾 Registrar Métrica en Array/]:::output
            %% End([🛑 Fin de Ronda]):::output
            End((🛑 Fin de Ronda)):::output
        end
    end

    %% ==========================================
    %% 🔀 CONEXIONES DEL FLUJO DE DATOS
    %% ==========================================
    Start --> Pay
    Pay ==> GenX

    %% Lógica de Búsqueda
    GenX --> CheckX
    CheckX -- SÍ (Sin hallazgos) ---> CalcBase
    CheckX -- NO (Encontró reliquias) ---> LoopStart

    %% Bucle de Pesaje
    LoopStart --> GenW
    GenW --> SumW
    SumW --> LoopEnd
    LoopEnd -. Continuar Bucle .-> LoopStart
    LoopEnd ==> |Todas pesadas| CalcBase

    %% Lógica de Tasación
    CalcBase --> GenB
    GenB --> CheckB
    CheckB -- SÍ (Bono Ídolo!) --> RewardDouble
    CheckB -- NO (Sin bono) --> RewardNormal

    %% Cierre y Salida
    RewardDouble ==> CalcNet
    RewardNormal ==> CalcNet
    CalcNet --> SaveResult
    SaveResult --> End

    %% ==========================================
    %% 🖌️ ESTILOS DE LOS SUBGRAPHS (Jerarquía)
    %% ==========================================
    style SYSTEM_WRAPPER fill:none,stroke:none
    
    style INIT fill:#fafafa,stroke:#e65100,stroke-width:3px,stroke-dasharray: 5 5
    style SIM fill:#fafafa,stroke:#1565c0,stroke-width:3px,stroke-dasharray: 5 5
    style STATS fill:#fafafa,stroke:#43a047,stroke-width:3px,stroke-dasharray: 5 5
    style LEGEND fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,stroke-dasharray: 5 5

    %% Estilos de los Sub-subgraphs (Anidados)
    style SEARCH fill:#f0f8ff,stroke:#5c6bc0,stroke-width:2px
    style WEIGH fill:#f3e5f5,stroke:#ab47bc,stroke-width:2px
    style APPRAISE fill:#e0f7fa,stroke:#00acc1,stroke-width:2px
```