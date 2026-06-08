#!/bin/bash
set -e

echo "📂 WORKDIR actuel : $(pwd)"
echo "📂 Contenu :"
ls -la

echo "📂 Recherche alembic.ini :"
find /app -name "alembic.ini" 2>/dev/null || echo "❌ alembic.ini introuvable !"

echo "📂 Recherche dossier alembic :"
find /app -name "env.py" 2>/dev/null || echo "❌ env.py introuvable !"

# Aller là où est alembic.ini
ALEMBIC_INI=$(find /app -name "alembic.ini" 2>/dev/null | head -1)

if [ -z "$ALEMBIC_INI" ]; then
    echo "❌ ERREUR : alembic.ini introuvable dans /app"
    echo "📂 Arbre complet :"
    find /app -type f | sort
    exit 1
fi

ALEMBIC_DIR=$(dirname "$ALEMBIC_INI")
echo "✅ alembic.ini trouvé : $ALEMBIC_INI"
echo "📂 Contenu du dossier alembic.ini :"
ls -la "$ALEMBIC_DIR"

echo "📄 Contenu de alembic.ini :"
cat "$ALEMBIC_INI"

cd "$ALEMBIC_DIR"
echo "⏳ Lancement des migrations..."
alembic -c "$ALEMBIC_INI" upgrade head
echo "✅ Migrations OK"