import uwoc31_11
import uwoc51_19
import uwoc51_27


def main():
    pT = range(-30, 20)
    samples = 10 ** 5

    print("51, 19")
    errRate_2 = uwoc51_19.genErrRate(pT, samples)


if __name__ == "__main__":
    main()
