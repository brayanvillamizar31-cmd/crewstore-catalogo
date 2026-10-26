#!/bin/bash
# ==============================================================================
# AGENTE DE OPTIMIZACIÓN & RENDIMIENTO UI/UX - CREWSTORE.CO
# Audita y optimiza fotos, tiempos de carga y velocidad móvil
# ==============================================================================

cd "$(dirname "$0")"

echo "=============================================="
echo " 🎨 AGENTE DE RENDIMIENTO & UI/UX"
echo "=============================================="
echo ""
echo "¿Qué deseas hacer?"
echo " 1) Solo auditar (ver peso y tiempos de carga)"
echo " 2) Optimizar todo (activar lazy loading + comprimir fotos)"
echo " 3) Salir"
echo ""
read -p "Elige una opción (1 o 2): " OPCION

if [ "$OPCION" = "1" ]; then
  python3 optimize_catalog.py --audit
elif [ "$OPCION" = "2" ]; then
  python3 optimize_catalog.py --all
else
  echo "Operación cancelada."
fi

echo ""
read -p "Presiona ENTER para cerrar..."
