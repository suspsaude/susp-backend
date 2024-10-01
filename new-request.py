import requests
import json

url = "https://elasticnes.saude.gov.br/kibana/api/reporting/v1/generate/immediate/csv_searchsource"
headers = {
    "Content-Type": "application/json",
    "kbn-xsrf": "true"
}
payload = {
    "browserTimezone": "Etc/GMT-3",
    "version": "8.8.2",
    "searchSource": {
        "query": {
            "query": "",
            "language": "kuery"
        },
        "fields": [
            {"field": "COMPETÊNCIA", "include_unmapped": "true"},
            {"field": "UF", "include_unmapped": "true"},
            {"field": "CÓDIGO DO MUNICÍPIO", "include_unmapped": "true"},
            {"field": "MUNICÍPIO", "include_unmapped": "true"},
            {"field": "CNES", "include_unmapped": "true"},
            {"field": "NOME FANTASIA", "include_unmapped": "true"},
            {"field": "TIPO NOVO DO ESTABELECIMENTO", "include_unmapped": "true"},
            {"field": "TIPO DO ESTABELECIMENTO", "include_unmapped": "true"},
            {"field": "SUBTIPO DO ESTABELECIMENTO", "include_unmapped": "true"},
            {"field": "GESTÃO", "include_unmapped": "true"},
            {"field": "CONVÊNIO SUS", "include_unmapped": "true"},
            {"field": "CATEGORIA NATUREZA JURÍDICA", "include_unmapped": "true"},
            {"field": "SERVIÇO", "include_unmapped": "true"},
            {"field": "SERVIÇO CLASSIFICAÇÃO", "include_unmapped": "true"},
            {"field": "SERVIÇO - AMBULATORIAL SUS", "include_unmapped": "true"},
            {"field": "SERVIÇO - AMBULATORIAL NÃO SUS", "include_unmapped": "true"},
            {"field": "SERVIÇO - HOSPITALAR SUS", "include_unmapped": "true"},
            {"field": "SERVIÇO - HOSPITALAR NÃO SUS", "include_unmapped": "true"},
            {"field": "SERVIÇO TERCEIRO", "include_unmapped": "true"},
            {"field": "STATUS DO ESTABELECIMENTO", "include_unmapped": "true"}
        ],
        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
        "sort": [{"COMPETÊNCIA": "desc"}],
        "filter": [
            {
                "meta": {
                    "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                    "params": {},
                    "field": "COMPETÊNCIA"
                },
                "query": {
                    "range": {
                        "COMPETÊNCIA": {
                            "format": "strict_date_optional_time",
                            "gte": "2007-06-30T21:00:00.000Z",
                            "lte": "2024-10-01T19:48:52.719Z"
                        }
                    }
                }
            }
        ],
        "parent": {
            "query": {
                "query": "",
                "language": "kuery"
            },
            "highlightAll": True,
            "filter": [
                {
                    "meta": {
                        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                        "key": "index_comp.keyword"
                    },
                    "query": {
                        "match_phrase": {
                            "index_comp.keyword": "202408"
                        }
                    }
                },
                {
                    "meta": {
                        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                        "key": "MUNICÍPIO.keyword"
                    },
                    "query": {
                        "match_phrase": {
                            "MUNICÍPIO.keyword": "SAO PAULO"
                        }
                    }
                },
                {
                    "meta": {
                        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                        "key": "STATUS DO ESTABELECIMENTO.keyword"
                    },
                    "query": {
                        "match_phrase": {
                            "STATUS DO ESTABELECIMENTO.keyword": "ATIVO"
                        }
                    }
                },
                {
                    "meta": {
                        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                        "type": "phrases",
                        "key": "CATEGORIA NATUREZA JURÍDICA.keyword",
                        "params": ["PÚBLICO", "SEM FINS LUCRATIVOS"]
                    },
                    "query": {
                        "bool": {
                            "should": [
                                {"match_phrase": {"CATEGORIA NATUREZA JURÍDICA.keyword": "PÚBLICO"}},
                                {"match_phrase": {"CATEGORIA NATUREZA JURÍDICA.keyword": "SEM FINS LUCRATIVOS"}}
                            ],
                            "minimum_should_match": 1
                        }
                    }
                }
            ],
            "parent": {
                "filter": [
                    {
                        "meta": {
                            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                            "params": {},
                            "field": "COMPETÊNCIA"
                        },
                        "query": {
                            "range": {
                                "COMPETÊNCIA": {
                                    "format": "strict_date_optional_time",
                                    "gte": "2007-06-30T21:00:00.000Z",
                                    "lte": "2024-10-01T19:48:52.719Z"
                                }
                            }
                        }
                    }
                ]
            }
        }
    },
    "columns": [
        "COMPETÊNCIA",
        "UF",
        "CÓDIGO DO MUNICÍPIO",
        "MUNICÍPIO",
        "CNES",
        "NOME FANTASIA",
        "TIPO NOVO DO ESTABELECIMENTO",
        "TIPO DO ESTABELECIMENTO",
        "SUBTIPO DO ESTABELECIMENTO",
        "GESTÃO",
        "CONVÊNIO SUS",
        "CATEGORIA NATUREZA JURÍDICA",
        "SERVIÇO",
        "SERVIÇO CLASSIFICAÇÃO",
        "SERVIÇO - AMBULATORIAL SUS",
        "SERVIÇO - AMBULATORIAL NÃO SUS",
        "SERVIÇO - HOSPITALAR SUS",
        "SERVIÇO - HOSPITALAR NÃO SUS",
        "SERVIÇO TERCEIRO",
        "STATUS DO ESTABELECIMENTO"
    ],
    "title": "EXTRATO DOS ESTABELECIMENTOS COM SERVIÇOS ESPECIALIZADOS"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.json())
