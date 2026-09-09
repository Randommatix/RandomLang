guardar jugador_vida = 100
guardar pociones = aleatorio(0, 3)
guardar turno = 1
guardar monstruo_vida = aleatorio(60, 220)

mostrar "=== ARENA DE MAZMORRAS ==="
mostrar "Aparece un monstruo con \monstruo_vida\ de vida."
mostrar "Llevas \pociones\ pociones en tu inventario."

mientras monstruo_vida > 0:
    si jugador_vida <= 0:
        mostrar "Has caído en el turno \turno\..."
        guardar monstruo_vida = 0

    si jugador_vida > 0:
        mostrar "--- Turno \turno\ (Tu vida: \jugador_vida\ | Monstruo: \monstruo_vida\) ---"

        
        guardar suerte_critico = aleatorio(1, 10)
        guardar dano_base = aleatorio(8, 15)

        si suerte_critico >= 8:
            guardar dano_jugador = dano_base * 2
            mostrar "¡GOLPE CRÍTICO! Haces \dano_jugador\ de daño al monstruo."

        si suerte_critico < 8:
            guardar dano_jugador = dano_base
            mostrar "Atacas al monstruo e infliges \dano_jugador\ de daño."

        guardar monstruo_vida = monstruo_vida - dano_jugador

        si monstruo_vida <= 0:
            mostrar "¡Derrotaste al monstruo!"
            guardar oro_ganado = aleatorio(10 * 2, 50 * 2)
            mostrar "¡Obtuviste \oro_ganado\ monedas de oro de recompensa!"

        si monstruo_vida > 0:
            
            guardar esquive = aleatorio(1, 5)

            si esquive == 5:
                mostrar "¡Esquivaste el ataque del monstruo completamente!"

            si esquive != 5:
                guardar dano_monstruo = aleatorio(5 + 2, 12 + 3)
                guardar jugador_vida = jugador_vida - dano_monstruo
                mostrar "El monstruo te golpea y te causa \dano_monstruo\ de daño."

            
            si jugador_vida <= 30:
                si pociones > 0:
                    guardar curacion = aleatorio(15, 30)
                    guardar jugador_vida = jugador_vida + curacion
                    guardar pociones = pociones - 1
                    mostrar "¡Poción de emergencia! Recuperas \curacion\ de vida. Te quedan \pociones\ pociones."

        guardar turno = turno + 1

mostrar "=== FIN DE LA COMBATE ==="
