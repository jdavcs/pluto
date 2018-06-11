from redact import redact_cc
from redact import redact_ssn

def main():
    redact_cc.RedactCC().run()
    redact_ssn.RedactSSN().run()

if __name__ == '__main__': main()
