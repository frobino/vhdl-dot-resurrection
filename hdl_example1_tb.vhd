-------------------------------------------------------------------------------
--! @file
--! @brief Test module
--!
--! Implements test module for doxygen
-------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

library work;
-------------------------------------------------------------------------------
--! Test entity declaration
-------------------------------------------------------------------------------
entity test_tb is
  generic
  (
    g_ClkFreqMHz     : real := 50.0
  );
   
end test_tb;
      
-------------------------------------------------------------------------------
--! Test architecture declaration
-------------------------------------------------------------------------------
architecture behavioral_test_tb of test_tb is

signal p_Clk,p_Rst : std_logic :=0;  
  
begin

  -- instance "test_1"
  
  --! @dot
  --! digraph example {
  --! node [shape=record, fontname=Helvetica, fontsize=10,color="red"];
  --! DataExtract [ label="Entity CDR_Top" URL="\ref CDR_Top"];
  --!   Serial_In -> Ser2Par;
  --!   Ser2Par -> DataExtract;
  --! }
  --! @enddot 
  test_1: entity work.test
    generic map (
      g_ClkFreqMHz => g_ClkFreqMHz)
    port map (
      p_Clk => p_Clk,
      p_Rst => p_Rst);  
 
end behavioral_test_tb;
