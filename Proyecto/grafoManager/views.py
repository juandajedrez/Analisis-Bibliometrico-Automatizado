from django.shortcuts import render
import json  # ✅ Importación necesaria

# Create your views here.
def grafo_view(request):
    data = {
        "nodes": [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        "links": [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
    }
    return render(request, "grafo.html", {"grafo_data": json.dumps(data)})