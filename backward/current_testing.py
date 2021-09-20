
#testing a jupyter notebook

#%%
print("exciting new worl!")

# %%
import numpy as np
newResults = np.load(r".\script_runs\opt_spec3-134_iter4_ncp_nightlybuild_cleanest.npz")
oldResults = np.load(r".\script_runs\opt_spec3-134_iter4_ncp_nightlybuild.npz")

np.testing.assert_allclose(newResults["all_mean_intensities"], oldResults["all_mean_intensities"])

for key in oldResults:
    try:
        print("\nevaluating: ",key)
        np.testing.assert_allclose(newResults[key], oldResults[key], rtol=1e-5)            
        print("shape: ", newResults[key].shape)
    except KeyError:
        print("KeyError: one of the results doesnt have this key")
    except AssertionError:
        print("Assertion Error")

# %%
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

syn = np.load(r"C:\Users\guijo\Desktop\work_repos\scatt_scripts\backward\script_runs\opt_spec3-134_iter4_ncp_nightlybuild_synthetic.npz")

ws = syn["all_fit_workspaces"][0, :, :-1]
ncp = syn["all_tot_ncp"][0]

x = np.linspace(0, 1, len(ncp[0]))
plt.figure(3)
spec_idx = 1
plt.plot(x, ws[spec_idx], label="synthetic ncp", linewidth = 2)
plt.plot(x, ncp[spec_idx], "--", label="fitted ncp", linewidth = 2)
plt.legend()
plt.show()

ncp_mask = np.isclose(ws, ncp, rtol=0.01, equal_nan = True)
plt.figure(0)
plt.imshow(ncp_mask, aspect="auto", cmap=plt.cm.RdYlGn, interpolation="nearest", norm=None)
plt.title("Comparison between ws and ncp")
plt.xlabel("TOF")
plt.ylabel("spectrums")
plt.show()
