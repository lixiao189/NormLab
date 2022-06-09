import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class WageCalculatorTest {

    @ParameterizedTest
    @CsvSource({"800, 40, 0, 20", "950, 45, 0, 20", "1280, 48, 8, 20"})
    void calculateWageParameterizedTest(int expected, int standard_hours, int holiday_hours, int hourly_wage) {
        assertEquals(expected, new WageCalculator().calculateWage(standard_hours, holiday_hours, hourly_wage));
    }
}
