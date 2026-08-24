import csv
from dataclasses import dataclass


@dataclass
class ReporteAuditoria:
    total_transacciones: int
    total_rechazadas: int
    total_alertas: int
    tasa_rechazo: float
    alertas_por_regla: list
    clientes_mas_senalados: list


def generar_reporte(transaction_repo, alert_repo, rejected_repo, top_n_clientes=5):
    "agrega lo ya persistido en la base de datos en un resumen de auditoria."
    total_transacciones = transaction_repo.count()
    total_rechazadas = rejected_repo.count()
    alertas_por_regla = alert_repo.count_by_rule()
    total_alertas = sum(conteo for _, conteo in alertas_por_regla)

    total_filas = total_transacciones + total_rechazadas
    tasa_rechazo = (total_rechazadas / total_filas) if total_filas else 0.0

    return ReporteAuditoria(
        total_transacciones=total_transacciones,
        total_rechazadas=total_rechazadas,
        total_alertas=total_alertas,
        tasa_rechazo=tasa_rechazo,
        alertas_por_regla=alertas_por_regla,
        clientes_mas_senalados=alert_repo.top_flagged_clients(top_n_clientes),
    )


def formatear_reporte_consola(reporte):
    "arma una tabla legible del reporte para mostrar en consola/logs."
    lineas = [
        "=== Reporte de auditoria LexData ===",
        f"Transacciones procesadas: {reporte.total_transacciones}",
        f"Filas rechazadas: {reporte.total_rechazadas}",
        f"Alertas generadas: {reporte.total_alertas}",
        f"Tasa de rechazo: {reporte.tasa_rechazo:.2%}",
        "",
        "Alertas por regla:",
    ]
    if reporte.alertas_por_regla:
        lineas.extend(f"  {regla}: {conteo}" for regla, conteo in reporte.alertas_por_regla)
    else:
        lineas.append("  (sin alertas)")

    lineas.append("")
    lineas.append("Clientes mas senalados:")
    if reporte.clientes_mas_senalados:
        lineas.extend(f"  client_id {client_id}: {conteo} alerta(s)" for client_id, conteo in reporte.clientes_mas_senalados)
    else:
        lineas.append("  (sin datos)")

    return "\n".join(lineas)


def exportar_csv(reporte, ruta_salida):
    "exporta el reporte a un CSV plano de tres columnas (seccion, clave, valor)."
    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["seccion", "clave", "valor"])
        writer.writerow(["resumen", "total_transacciones", reporte.total_transacciones])
        writer.writerow(["resumen", "total_rechazadas", reporte.total_rechazadas])
        writer.writerow(["resumen", "total_alertas", reporte.total_alertas])
        writer.writerow(["resumen", "tasa_rechazo", f"{reporte.tasa_rechazo:.4f}"])

        for regla, conteo in reporte.alertas_por_regla:
            writer.writerow(["alertas_por_regla", regla, conteo])

        for client_id, conteo in reporte.clientes_mas_senalados:
            writer.writerow(["clientes_mas_senalados", client_id, conteo])
