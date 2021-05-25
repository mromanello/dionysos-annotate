function makePostRequest(url, data) {
    return new Request(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
}

function save_unit_modifs(unit_id) {
    let formData = $("#changeUnit" + unit_id).serializeArray()
    let request = makePostRequest('/saveUnitModifs', formData)
    fetch(request).then(response => response.json()).then(
        data => {
            let table = $('#unitTable').DataTable()
            let french_text = data['french_text']
            var d = table.row().data();
            d['french_text'] = french_text
            table
                .row()
                .data(d)
                .draw();
        })
    return true
}


french_data_tables_translation = {
    "emptyTable": "Aucune donnée disponible dans le tableau",
    "lengthMenu": "Afficher _MENU_ éléments",
    "loadingRecords": "Chargement...",
    "processing": "Traitement...",
    "zeroRecords": "Aucun élément correspondant trouvé",
    "paginate": {
        "first": "Premier",
        "last": "Dernier",
        "previous": "Précédent",
        "next": "Suiv"
    },
    "aria": {
        "sortAscending": ": activer pour trier la colonne par ordre croissant",
        "sortDescending": ": activer pour trier la colonne par ordre décroissant"
    },
    "select": {
        "rows": {
            "_": "%d lignes sélectionnées",
            "0": "Aucune ligne sélectionnée",
            "1": "1 ligne sélectionnée"
        },
        "1": "1 ligne selectionnée",
        "_": "%d lignes selectionnées",
        "cells": {
            "1": "1 cellule sélectionnée",
            "_": "%d cellules sélectionnées"
        },
        "columns": {
            "1": "1 colonne sélectionnée",
            "_": "%d colonnes sélectionnées"
        }
    },
    "autoFill": {
        "cancel": "Annuler",
        "fill": "Remplir toutes les cellules avec <i>%d<\/i>",
        "fillHorizontal": "Remplir les cellules horizontalement",
        "fillVertical": "Remplir les cellules verticalement",
        "info": "Exemple de remplissage automatique"
    },
    "searchBuilder": {
        "conditions": {
            "date": {
                "after": "Après le",
                "before": "Avant le",
                "between": "Entre",
                "empty": "Vide",
                "equals": "Egal à",
                "not": "Différent de",
                "notBetween": "Pas entre",
                "notEmpty": "Non vide"
            },
            "number": {
                "between": "Entre",
                "empty": "Vide",
                "equals": "Egal à",
                "gt": "Supérieur à",
                "gte": "Supérieur ou égal à",
                "lt": "Inférieur à",
                "lte": "Inférieur ou égal à",
                "not": "Différent de",
                "notBetween": "Pas entre",
                "notEmpty": "Non vide"
            },
            "string": {
                "contains": "Contient",
                "empty": "Vide",
                "endsWith": "Se termine par",
                "equals": "Egal à",
                "not": "Différent de",
                "notEmpty": "Non vide",
                "startsWith": "Commence par"
            },
            "array": {
                "equals": "Egal à",
                "empty": "Vide",
                "contains": "Contient",
                "not": "Différent de",
                "notEmpty": "Non vide",
                "without": "Sans"
            }
        },
        "add": "Ajouter une condition",
        "button": {
            "0": "Recherche avancée",
            "_": "Recherche avancée (%d)"
        },
        "clearAll": "Effacer tout",
        "condition": "Condition",
        "data": "Donnée",
        "deleteTitle": "Supprimer la règle de filtrage",
        "logicAnd": "Et",
        "logicOr": "Ou",
        "title": {
            "0": "Recherche avancée",
            "_": "Recherche avancée (%d)"
        },
        "value": "Valeur"
    },
    "searchPanes": {
        "clearMessage": "Effacer tout",
        "count": "{total}",
        "title": "Filtres actifs - %d",
        "collapse": {
            "0": "Volet de recherche",
            "_": "Volet de recherche (%d)"
        },
        "countFiltered": "{shown} ({total})",
        "emptyPanes": "Pas de volet de recherche",
        "loadMessage": "Chargement du volet de recherche..."
    },
    "buttons": {
        "copyKeys": "Appuyer sur ctrl ou u2318 + C pour copier les données du tableau dans votre presse-papier.",
        "collection": "Collection",
        "colvis": "Visibilité colonnes",
        "colvisRestore": "Rétablir visibilité",
        "copy": "Copier",
        "copySuccess": {
            "1": "1 ligne copiée dans le presse-papier",
            "_": "%ds lignes copiées dans le presse-papier"
        },
        "copyTitle": "Copier dans le presse-papier",
        "csv": "CSV",
        "excel": "Excel",
        "pageLength": {
            "-1": "Afficher toutes les lignes",
            "1": "Afficher 1 ligne",
            "_": "Afficher %d lignes"
        },
        "pdf": "PDF",
        "print": "Imprimer"
    },
    "decimal": ",",
    "info": "Affichage de _START_ à _END_ sur _TOTAL_ éléments",
    "infoEmpty": "Affichage de 0 à 0 sur 0 éléments",
    "infoThousands": ".",
    "search": "Rechercher:",
    "searchPlaceholder": "...",
    "thousands": ".",
    "infoFiltered": "(filtrés depuis un total de _MAX_ éléments)",
    "datetime": {
        "previous": "Précédent",
        "next": "Suivant",
        "hours": "Heures",
        "minutes": "Minutes",
        "seconds": "Secondes",
        "unknown": "-",
        "amPm": [
            "am",
            "pm"
        ]
    },
    "editor": {
        "close": "Fermer",
        "create": {
            "button": "Nouveaux",
            "title": "Créer une nouvelle entrée",
            "submit": "Envoyer"
        },
        "edit": {
            "button": "Editer",
            "title": "Editer Entrée",
            "submit": "Modifier"
        },
        "remove": {
            "button": "Supprimer",
            "title": "Supprimer",
            "submit": "Supprimer"
        },
        "error": {
            "system": "Une erreur système s'est produite"
        },
        "multi": {
            "title": "Valeurs Multiples",
            "restore": "Rétablir Modification"
        }
    }
}

function define_unit_table(project_id) {
    $(document).ready(function () {
        $('#unitTable').DataTable({
            deferRender: true,
            bStateSave: true,
            language: french_data_tables_translation,
            lengthMenu: [1, 5, 10, 50, 100],
            ajax: "/unitsJson?id=" + project_id,
            scrollY: "600px",
            scrollCollapse: true,
            scroller: true,
            columns: [
                {"data": "unit_num"},
                {"data": "cite"},
                {"data": "speaker"},
                {
                    "data": "mouvements",
                    "render": function (data) {
                        mouvements = data.split("-")
                        html = ""
                        mouvements.forEach(mouv => html += "<div>" + mouv + "</div>")
                        return html;
                    }
                },
                {
                    "data": "text",
                    "orderable": false,
                    "render": function (data, type, row) {
                        html = data
                        if (row.french_text) {
                            html += "<br>"
                            html += `<b> ${row.french_text} </b>`
                        }
                        html += ` <form id="changeUnit${row.id}" action="/saveUnitModifs" method="post">
                                        <div class="form-group">
                                            <input type="hidden" name="unit_id" value=${row.id}>
                                        </div>
                                        <div class="form-group">
                                            <input type="hidden" name="unit_num" value=${row.unit_num}>
                                        </div>
                                        <div class="form-group mb-1">
                                            <textarea type="textarea" class="form-control", name="french_text"
                                                rows="2" required>${row.french_text}</textarea>
                                        </div>
                                </form>
                                <button id="submitUnit${row.id}" onclick="save_unit_modifs(${row.id})"  class="btn btn-success float-end">Enregistrer </button>
                        `
                        return html;
                    }
                },
            ]
        });
    });
}


