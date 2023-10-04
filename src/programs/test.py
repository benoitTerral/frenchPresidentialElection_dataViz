import pickle
import os

pickle_departements = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/df_departements.pkl"
pickle_communes = (
    f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/df_communes.pkl"
)
pickle_communes_location = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/communes_location.pkl"


with open(pickle_departements, "rb") as departements, open(
    pickle_communes, "rb"
) as communes, open(pickle_communes_location, "rb") as communes_location:
    df_departements = pickle.load(departements)
    df_communes = pickle.load(communes)
    df_communes_location = pickle.load(communes_location)

# print(df_communes_location.dtypes)
# print(df_communes["2022"].dtypes)
print(df_communes["2022"][df_communes["2022"]["nomcommune"] == "TIVIERS"])
