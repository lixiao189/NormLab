/**
public class RomanNumeralTest {

    @Test
    void convertSingleDigit() {
        RomanNumeral roman = new RomanNumeral();
        int result = roman.convert("C");

        assertEquals(100, result);
    }

    @Test
    void convertNumberWithDifferentDigits() {
        RomanNumeral roman = new RomanNumeral();
        int result = roman.convert("CCXVI");

        assertEquals(216, result);
    }

    @Test
    void convertNumberWithSubtractiveNotation() {
        RomanNumeral roman = new RomanNumeral();
        int result = roman.convert("XL");

        assertEquals(40, result);
    }
}
*/

/*

public class RomanNumeralTest {

    /**
     * Method: romanToInt(String s)
     */
 /*   @Test
    public void testRomanToInt() throws Exception {
        int result = new RomanNumeral().romanToInt("II");
        assertEquals(2, result);
    }

    @Test
    void singleDigit() {
        assertEquals(1, new RomanNumeral().romanToInt("I"));
        assertEquals(5, new RomanNumeral().romanToInt("V"));
        assertEquals(10, new RomanNumeral().romanToInt("X"));
        assertEquals(50, new RomanNumeral().romanToInt("L"));
        assertEquals(100, new RomanNumeral().romanToInt("C"));
        assertEquals(500, new RomanNumeral().romanToInt("D"));
        assertEquals(1000, new RomanNumeral().romanToInt("M"));
    }

    //TODO: Your answer goes here!!!
    @ParameterizedTest
    @CsvSource({"I,1", "V,5", "X,10", "L,50", "C, 100", "D, 500", "M, 1000"})
    void singleDigitParameterizedTest(String input, int expected) {
       RomanNumeral toInt = new RomanNumeral();

       int result = toInt.romanToInt(input);
       assertEquals(expected, result);
    }
}*/
