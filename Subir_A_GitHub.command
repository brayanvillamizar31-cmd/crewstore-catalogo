#!/bin/bash
# ==============================================================================
# AGENTE CI/CD & DESPLIEGUE AUTOMÁTICO - CREWSTORE.CO
# Valida la integridad de la tienda, registra cambios y publica en GitHub y Vercel
# ==============================================================================

cd "$(dirname "$0")"

echo "=============================================="
echo " 🚀 DESPLIEGUE AUTOMÁTICO CREWSTORE.CO (GITHUB + VERCEL + SUPABASE)"
echo "=============================================="
echo ""

python3 deploy_validator.py
if [ $? -ne 0 ]; then
  echo "❌ El despliegue se canceló porque fallaron las validaciones."
  exit 1
fi

git config user.name "brayanvillamizar31-cmd"
git config user.email "339623759+brayanvillamizar31-cmd@users.noreply.github.com"
git add -A

if ! git diff --cached --quiet; then
  FECHA=$(date "+%Y-%m-%d %H:%M:%S")
  git commit -m "Actualización automática en tiempo real: $FECHA"
  echo "✅ Cambios guardados localmente."
fi

if git push origin main; then
  echo "🎉 ¡Sincronizado en tiempo real con GitHub y Vercel!"
else
  echo "⚠️ Error al hacer push a GitHub."
fi
