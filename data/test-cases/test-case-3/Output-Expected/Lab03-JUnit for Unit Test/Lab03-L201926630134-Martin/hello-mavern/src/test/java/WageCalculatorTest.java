import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class WageCalculatorTest {
    @ParameterizedTest
    @CsvSource({"40,0,800", "45,0,950", "48,8,1280"})
    void getWages( int standardHours, int holidayHours, double expected) {
        WageCalculator wage = new WageCalculator();

        double result = wage.CalculateWage(standardHours, holidayHours);
        assertEquals(expected, result);
    }
}
