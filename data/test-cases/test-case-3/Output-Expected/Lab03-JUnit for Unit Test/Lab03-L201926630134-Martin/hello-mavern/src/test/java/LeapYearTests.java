import org.testng.annotations.Test;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class LeapYearTests {

    private final LeapYear leapYear = new LeapYear();

    @Test
    public void divisibleBy4_notDivisibleBy100() {
        boolean leap = leapYear.isLeapYear(2016);
        assertTrue(leap);
    }

    @Test
    public void divisibleBy4_100_400() {
        boolean leap = leapYear.isLeapYear(2000);
        assertTrue(leap);
    }

    @Test
    public void notDivisibleBy4() {
        boolean leap = leapYear.isLeapYear(39);
        assertFalse(leap);
    }

    @Test
    public void divisibleBy4_and_100_not_400() {
        boolean leap = leapYear.isLeapYear(1900);
        assertFalse(leap);
    }
}
