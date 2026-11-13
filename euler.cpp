// ============================================================================
//  euler.cpp  —  Ciclo Euleriano con el algoritmo de Hierholzer  (O(V + E))
//  CS2023 - Proyecto 2 - Animando Estructuras de Datos (UTEC)
//
//  Lee un grafo NO dirigido desde la entrada estandar y escribe en la salida
//  estandar un JSON con:
//    - el grafo (aristas y grados)
//    - si existe o no un ciclo euleriano (y por que)
//    - el ciclo como secuencia de vertices
//    - el orden en que se recorren las aristas (para animar paso a paso)
//
//  Formato de entrada:
//    n m                (n = numero de vertices, m = numero de aristas)
//    u1 v1              (una arista por linea, vertices 0..n-1)
//    ...
//    um vm
// ============================================================================
#include <iostream>
#include <vector>
#include <utility>
#include <stack>
#include <algorithm>
#include <string>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m) || n < 0 || m < 0) return 1;

    vector<pair<int,int>> edges(m);
    vector<vector<pair<int,int>>> adj(n);   // adj[u] = lista de (vecino, id_arista)
    vector<int> degree(n, 0);

    for (int i = 0; i < m; i++) {
        int u, v;
        if (!(cin >> u >> v) || u < 0 || v < 0 || u >= n || v >= n) {
            cerr << "Entrada invalida: vertice fuera de rango.\n";
            return 1;
        }
        edges[i] = {u, v};
        adj[u].push_back({v, i});
        adj[v].push_back({u, i});
        degree[u]++;
        degree[v]++;
    }

    // ---- Condicion 1: todos los vertices deben tener grado par ----
    bool allEven = true;
    for (int i = 0; i < n; i++)
        if (degree[i] % 2 != 0) allEven = false;

    // ---- Condicion 2: los vertices con aristas deben estar conectados ----
    int start = -1;
    for (int i = 0; i < n; i++)
        if (degree[i] > 0) { start = i; break; }

    bool connected = true;
    if (start != -1) {
        vector<bool> visited(n, false);
        stack<int> st;
        st.push(start);
        visited[start] = true;
        while (!st.empty()) {
            int u = st.top(); st.pop();
            for (auto [v, id] : adj[u])
                if (!visited[v]) { visited[v] = true; st.push(v); }
        }
        for (int i = 0; i < n; i++)
            if (degree[i] > 0 && !visited[i]) connected = false;
    }

    bool hasCircuit = (m > 0) && allEven && connected;
    string reason;
    if (m == 0)           reason = "El grafo no tiene aristas.";
    else if (!allEven)    reason = "Hay vertices de grado impar: no existe ciclo euleriano.";
    else if (!connected)  reason = "El grafo no es conexo: no existe ciclo euleriano.";
    else                  reason = "Conexo y todos los grados pares: existe ciclo euleriano.";

    // Eventos compactos: O(1) por evento, sin copiar la pila completa.
    struct Event { string type; int u, v, edge; };
    vector<Event> events;

    // ---- Algoritmo de Hierholzer ----
    vector<int> circuit;       // secuencia de vertices del ciclo
    vector<int> edgeOrder;     // orden en que se recorren las aristas (ids)
    if (hasCircuit) {
        vector<bool> usedEdge(m, false);
        vector<int> ptr(n, 0);              // puntero a la sig. arista por explorar en cada vertice
        stack<int> st;
        st.push(start);
        vector<int> incoming;
        incoming.push_back(-1);
        events.push_back({"start", start, -1, -1});
        while (!st.empty()) {
            int u = st.top();
            while (ptr[u] < (int)adj[u].size() && usedEdge[adj[u][ptr[u]].second]) ptr[u]++;
            if (ptr[u] == (int)adj[u].size()) {
                circuit.push_back(u);       // sin aristas libres: se cierra el sub-ciclo
                st.pop();
                int enteredBy = incoming.back();
                incoming.pop_back();
                if (enteredBy != -1) edgeOrder.push_back(enteredBy);
                events.push_back({"finish", u, -1, enteredBy});
            } else {
                auto [v, id] = adj[u][ptr[u]];
                usedEdge[id] = true;        // consumimos la arista
                ptr[u]++;
                st.push(v);
                incoming.push_back(id);
                events.push_back({"traverse", u, v, id});
            }
        }
        reverse(circuit.begin(), circuit.end());

        reverse(edgeOrder.begin(), edgeOrder.end());
        events.push_back({"reverse", -1, -1, -1});
    }

    // ---- Salida JSON ----
    cout << "{\n";
    cout << "  \"n\": " << n << ",\n";

    cout << "  \"edges\": [";
    for (int i = 0; i < m; i++) {
        cout << "[" << edges[i].first << "," << edges[i].second << "]";
        if (i + 1 < m) cout << ", ";
    }
    cout << "],\n";

    cout << "  \"degrees\": [";
    for (int i = 0; i < n; i++) { cout << degree[i]; if (i + 1 < n) cout << ", "; }
    cout << "],\n";

    cout << "  \"has_circuit\": " << (hasCircuit ? "true" : "false") << ",\n";
    cout << "  \"reason\": \"" << reason << "\",\n";

    cout << "  \"circuit\": [";
    for (size_t i = 0; i < circuit.size(); i++) { cout << circuit[i]; if (i + 1 < circuit.size()) cout << ", "; }
    cout << "],\n";

    cout << "  \"edge_order\": [";
    for (size_t i = 0; i < edgeOrder.size(); i++) { cout << edgeOrder[i]; if (i + 1 < edgeOrder.size()) cout << ", "; }
    cout << "],\n";
    cout << "  \"events\": [";
    for (size_t i = 0; i < events.size(); ++i) {
        const auto &e = events[i];
        if (i) cout << ",";
        cout << "\n    {\"type\":\"" << e.type
             << "\",\"u\":" << e.u << ",\"v\":" << e.v
             << ",\"edge\":" << e.edge << "}";
    }
    cout << "\n  ]\n";

    cout << "}\n";
    return 0;
}
