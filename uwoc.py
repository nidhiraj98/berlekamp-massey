import uwoc31_11
import uwoc51_19
import uwoc51_27
import uwocUncoded
import matplotlib.pyplot as plt
import pickle

def main():
    pT = range(-30, 20)
    samples = 10 ** 6
    print("Uncoded")
    errRateUncoded = uwocUncoded.genErrRate(pT, samples)
    pickle_it("./temp-var/errRateUncoded", errRateUncoded)
    # errRateUncoded = unpickle_it("errRateUncoded")
    plt.semilogy(pT, errRateUncoded, color = "black")

    print("31, 11")
    errRate_1 = uwoc31_11.genErrRate(pT, samples)
    pickle_it("./temp-var/errRate31_11", errRate_1)
    # errRate_1 = unpickle_it("errRate31_11")
    plt.semilogy(pT, errRate_1, color = 'red')

    print("51, 19")
    errRate_2 = uwoc51_19.genErrRate(pT, samples)
    pickle_it("./temp-var/errRate51_19", errRate_2)
    plt.semilogy(pT, errRate_2, color = 'blue')


    print("51, 27")
    errRate_3 = uwoc51_27.genErrRate(pT, samples)
    pickle_it("./temp-var/errRate51_27", errRate_3)
    plt.semilogy(pT, errRate_3, color = 'green')

    plt.title("BER Analysis for various BCH Codes")
    plt.xlabel("Signal to Noise Ratio")
    plt.ylabel("Bit Error Rate")
    plt.legend(['Uncoded', '(31, 11) BCH Code', '(51, 19) BCH Code', '(51, 27) BCH Code'])
    plt.show()

def pickle_it(file_name,  data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def unpickle_it(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    main()