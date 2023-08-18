import os
import sys

import pandas as pd


def main(opencoesione_filepath: str, list_cup_filepath, dipe_feedback: str):
    """
    Esegue il controllo CUP utilizzando i dati forniti.

    Parameters:
        opencoesione_filepath (str): file .zip con dati OpenCoesione.
        list_cup_filepath (str): file con estrazione dei CUP da PAdigitale.
        dipe_feedback (str): Il nome della cartella contenente i file dal DIPE.

    Output:
        file CUP_ANALYSIS.xls e KPI_aggregati.csv con controllo CUP.
    """

    # opencoesione file
    df_OC = pd.read_csv(
        "data/" + opencoesione_filepath,
        compression="zip",
        sep=";",
        quotechar='"',
        low_memory=False,
        usecols=[
            "COD_LOCALE_PROGETTO",
            "CUP",
            "OC_TITOLO_PROGETTO",
            "OC_DESCR_CICLO",
            "OC_COD_CICLO",
            "OC_TEMA_SINTETICO",
            "FONDO_COMUNITARIO",
            "OC_CODICE_PROGRAMMA",
            "OC_DESCRIZIONE_PROGRAMMA",
            "COD_STRUMENTO",
            "DESCR_STRUMENTO",
            "OC_STATO_FINANZIARIO",
            "OC_STATO_PROGETTO",
            "OC_STATO_PROCEDURALE",
        ],
        header=0,
        # nrows=10
    )

    # feedback DIPE
    DIRNAME = "data/" + dipe_feedback
    dfs = []
    lenghts = []
    for filename in os.listdir(DIRNAME):
        if filename.endswith(".xlsx"):
            with pd.ExcelFile(os.path.join(DIRNAME, filename)) as fl:
                data = pd.read_excel(fl, sheet_name=0, header=0).copy()
                dfs.append(data)
                lenghts.append(len(data))
    df = pd.concat(dfs, axis=0, ignore_index=True).drop_duplicates()

    assert df.CODICE_CUP.duplicated().sum() == 0

    # lista CUP da Salesforce (estrazione)
    with pd.ExcelFile(os.path.join("data", list_cup_filepath)) as fl:
        df_pad2026 = pd.read_excel(fl, sheet_name=0).copy()

    col_list = df_pad2026.columns
    df_pad2026.columns = [col.upper().replace(" ", "_") for col in col_list]

    assert df_pad2026.columns == [
        "CODICE_CUP",
        "NOME_DECRETO",
        "MISURA",
        "APPLYING_ORGANIZATION:_TIPOLOGIA_ENTE",
    ]

    tmp_df = df_pad2026.merge(df, on="CODICE_CUP", how="left").copy()
    assert len(tmp_df) == len(df_pad2026)
    df_OC = df_OC.drop_duplicates(subset="CUP", keep="last").copy()

    # Primi check
    # CUP double funding
    DOUBLE_FUNDING_CUP = pd.merge(
        df_OC["CUP"],
        tmp_df["CODICE_CUP"],
        left_on="CUP",
        right_on="CODICE_CUP",
        how="inner",
        validate="1:m",
    ).CUP.unique()
    # CUP double project
    DOUBLE_REQUEST_CUP = (
        tmp_df.groupby(by="CODICE_CUP")
        .filter(lambda x: len(x) > 1)
        .sort_values(by="CODICE_CUP")
        .CODICE_CUP.unique()
    )
    # CUP non esistente nei sistemi DIPE
    na_cup_condition = tmp_df.STATO_PROGETTO == "CUP INESISTENTE"
    MISSING_CUP = tmp_df[na_cup_condition].CODICE_CUP.unique()
    # Template mancante
    MISSING_TEMPLATE = tmp_df[tmp_df.TEMPLATE.isna()].CODICE_CUP.unique()
    # Template errato
    map_sheet2template = (
        tmp_df[["NOME_DECRETO", "TEMPLATE"]]
        .groupby(["NOME_DECRETO"])
        .TEMPLATE.agg(pd.Series.mode)
        .to_dict()
    )
    WRONG_TEMPLATE = []
    WRONG_TEMPLATE = tmp_df[
        tmp_df.NOME_DECRETO.replace(map_sheet2template) != tmp_df.TEMPLATE
    ].CODICE_CUP.unique()

    def classify_CUP(CUP: str):
        """
        Classifica il CUP in base a una scala di priorità.

        Parameters:
            CUP (str): Il codice CUP da classificare.

        Returns:
            str: La classificazione del CUP.
        """

        if CUP in DOUBLE_FUNDING_CUP:
            return "CUP già presente in OPEN COESIONE"
        elif CUP in MISSING_CUP:
            return "CUP NON PRESENTE NEL FEEDBACK DIPE"
        elif CUP in DOUBLE_REQUEST_CUP:
            return "CUP PRESENTE IN PIU' CANDIDATURE"
        elif CUP in MISSING_TEMPLATE:
            return "TEMPLATE MANCANTE"
        elif CUP in WRONG_TEMPLATE:
            return "POSSIBILE TEMPLATE ERRATO"
        else:
            return "NESSUN PROBLEMA RISCONTRATO AL MOMENTO"

    tmp_df["CLASSIFICAZIONE_ISSUE_CUP"] = tmp_df.CODICE_CUP.apply(classify_CUP)

    print(tmp_df.CODICE_CUP.count())
    print(len(df_pad2026))
    # crea aggregati
    tmp_df.groupby(by=["CLASSIFICAZIONE_ISSUE_CUP"]).CODICE_CUP.count().to_csv(
        "data/KPI_aggregati.csv", index=False
    )

    tmp_df.to_excel("../data/02_primary/CUP_ANALYSIS.xlsx", index=False)

    def fake_function1():
        """fake function"""
        pass

    def fake_function2():
        """fake function"""
        pass


if __name__ == "__main__":
    """
    Esegue il controllo CUP utilizzando i file specificati.
    """
    args = sys.argv[1:]
    # args[0] = "progetti_esteso_20230430.zip"
    # arg2 = "CUP"
    # arg3 = "Estrazione CUP-2023-07-19-09-01-50.xlsx"
    main(args[0], args[1], args[2])
