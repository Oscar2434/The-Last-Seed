# 🌱 The Last Seed: El Guardián del Bosque

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Age](https://img.shields.io/badge/Age%203--12-Educational-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

**The Last Seed** es un videojuego educativo desarrollado en Python que combina acción, estrategia y conciencia ecológica. A través de dos niveles únicos, los jugadores se convierten en guardianes del bosque con la misión de proteger la naturaleza mientras aprenden valiosas lecciones sobre conservación ambiental.

## 🎮 Características Principales

### 🎯 **Sistema de Niveles Completos**
- **Nivel 1**: Defensa del Ecosistema - Protege el árbol central de leñadores
- **Nivel 2**: Laberinto de la Naturaleza - Recolecta recursos educativos en un laberinto
- **Sistema de progresión** entre niveles
- **Objetivos claros** y mensajes educativos

### 👥 **Selección de Personaje y Dificultad**
- **Elección entre Niño y Niña** con sprites únicos
- **Sistema de dificultad ajustable** (Normal/Avanzado)
- **Menú interactivo** con efectos hover
- **Configuración persistente** entre niveles

### 🌳 **Mecánicas de Juego Avanzadas**
- **Sistema de salud visual** para árboles con barras de vida
- **Recursos animados** (agua con efectos de animación)
- **Efectos de partículas** (fuego en árboles dañados)
- **Sistema de inventario** para recursos recolectados

## 🏗️ Arquitectura del Proyecto


## 🎯 Objetivos por Nivel

### 🌳 Nivel 1: Defensa del Ecosistema
**Victoria:**
- ✅ Mantener el árbol central con vida
- ✅ Conservar al menos 3 árboles normales vivos  
- ✅ Sobrevivir hasta que termine el tiempo

**Mecánicas:**
- **Recolecta cubetas de agua** que aparecen aleatoriamente
- **Cura árboles dañados** presionando `E` cerca de ellos
- **Evita leñadores** que atacan árboles continuamente
- **Sistema de fuego** en árboles con salud crítica

### 🏰 Nivel 2: Laberinto de la Naturaleza
**Victoria:**
- ✅ Recolectar 3 recursos educativos:
  - 🍌 Cáscara de plátano (composta)
  - 🥚 Cáscara de huevo (minerales) 
  - 💧 Agua (hidratación)
- ✅ Entregarlos al árbol central presionando `E`
- ✅ Evitar ser capturado por fantasmas

**Características Únicas:**
- **Laberinto procedural** con diferentes tipos de muros
- **Diálogos educativos** que explican beneficios ecológicos
- **Fantasmas inteligentes** que persiguen al jugador
- **Temporizador** con pausas durante diálogos

## 👾 Sistema de Enemigos

### 🔥 Leñadores (Nivel 1)
- **IA de ataque a árboles**: Eligen objetivos estratégicamente
- **Sistema de animaciones**: 6 estados diferentes
- **Detección de colisiones**: Evitan obstáculos y otros árboles
- **Ataque coordinado**: Múltiples enemigos atacan diferentes objetivos

### 👻 Fantasmas (Nivel 2)
- **Persecución inteligente**: Siguen al jugador por el laberinto
- **Evitación de obstáculos**: Navegan alrededor de muros
- **Sprites direccionales**: Cambian según la dirección del movimiento
- **Detección de captura**: Sistema de colisión preciso

## 🎨 Sistema Gráfico y Animaciones

### 🏃 Animaciones de Personaje
- **Spritesheet completo**: 4 direcciones × 3 frames cada una
- **Transiciones suaves**: Entre estados de movimiento y idle
- **Flip horizontal**: Optimización de recursos para dirección izquierda
- **Sistema de timing**: Frame rate consistente

### 🔥 Efectos Visuales
- **Fuego animado**: Partículas en árboles dañados (5 frames)
- **Agua animada**: Cubetas con efectos de reflejo (10 frames) 
- **Barra de vida**: Visualización clara del estado de árboles
- **Interfaz de usuario**: Inventario y temporizador no intrusivos

## 🎮 Controles

| Acción | Tecla | Nivel 1 | Nivel 2 |
|--------|-------|---------|---------|
| **Movimiento** | `↑` `↓` `←` `→` | ✅ | ✅ |
| **Interactuar/Curar** | `E` | ✅ | ✅ |
| **Continuar diálogos** | `ESPACIO` | ❌ | ✅ |
| **Recolectar recursos** | Automático | ✅ | ✅ |

## ⚙️ Sistema de Dificultad

### 🎯 Configuración por Nivel

**Nivel 1:**
- **Normal**: Velocidad 1, Daño 2, Tiempo 90s, 5 enemigos
- **Avanzado**: Velocidad 2, Daño 6, Tiempo 60s, 8 enemigos

**Nivel 2:**
- **Normal**: 2 fantasmas en posiciones estratégicas
- **Avanzado**: 3 fantasmas con cobertura completa

## 🌟 Valor Educativo

### 📚 Aprendizaje Integrado
- **Compostaje**: Cáscaras de plátano como abono orgánico
- **Minerales naturales**: Cáscaras de huevo como fuente de calcio
- **Conservación del agua**: Importancia de la hidratación para plantas
- **Reforestación**: Protección y cuidado de árboles
- **Biodiversidad**: Equilibrio en el ecosistema

### 💡 Mensajes Educativos
- Diálogos contextuales que explican conceptos ecológicos
- Sistema de retroalimentación inmediata
- Aprendizaje through gameplay sin interrupciones forzadas

## 🛠️ Instalación y Ejecución

### Prerrequisitos
```bash
# Python 3.8 o superior
python --version

# Instalar Pygame
pip install pygame

# Tener Python 3.8 o superior instalado
python --version
