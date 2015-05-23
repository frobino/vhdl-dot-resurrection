library IEEE;
use IEEE.std_logic_1164.all;

entity top_level is
  port (
    clk, reset                     : in  std_logic;
    abusX                          : out std_logic_vector(15 downto 0);
    dbusX                          : out std_logic_vector(15 downto 0);
    mem_enDX, mem_rwX              : out std_logic;
    pc_enAX, pc_ldX, pc_incX       : out std_logic;
    ir_enAX, ir_enDX, ir_ldX       : out std_logic;
    iar_enAX, iar_ldX              : out std_logic;
    acc_enDX, acc_ldX, acc_selAluX : out std_logic;
    acc_QX                         : out std_logic_vector(15 downto 0);
    alu_accZX                      : out std_logic;
    alu_opX                        : out std_logic_vector(1 downto 0)
    );
end top_level;

architecture topArch of top_level is

  component program_counter
    port (
      clk, en_A, ld, inc, reset : in  std_logic;
      aBus                      : out std_logic_vector(15 downto 0);
      dBus                      : in  std_logic_vector(15 downto 0)
      );
  end component;

  component instruction_register
    port (
      clk, en_A, en_D, ld, reset          : in    std_logic;
      aBus                                : out   std_logic_vector(15 downto 0);
      dBus                                : out std_logic_vector(15 downto 0);
      load, store, add, neg, halt, branch : out   std_logic;
      cbranch, iload, istore, dload, dadd : out   std_logic
      );
  end component;

  component indirect_addr_register
    port (
      clk, en_A, ld, reset : in  std_logic;
      aBus                 : out std_logic_vector(15 downto 0);
      dBus                 : in  std_logic_vector(15 downto 0)
      );
  end component;

  component accumulator
    port (
      clk, en_D, ld, selAlu, reset : in    std_logic;
      aluD                         : in    std_logic_vector(15 downto 0);
      dBus                         : out std_logic_vector(15 downto 0);
      q                            : out   std_logic_vector(15 downto 0)
      );
  end component;

  component alu
    port (
      op     : in  std_logic_vector(1 downto 0);
      accD   : in  std_logic_vector(15 downto 0);
      dBus   : in  std_logic_vector(15 downto 0);
      result : out std_logic_vector(15 downto 0);
      accZ   : out std_logic
      );
  end component;

  component ram
    port (
      r_w, en, reset : in    std_logic;
      aBus           : in    std_logic_vector(15 downto 0);
      dBus           : out std_logic_vector(15 downto 0)
      );
  end component;

  component controller
    port (
      clk, reset                   : in  std_logic;
      mem_enD, mem_rw              : out std_logic;
      pc_enA, pc_ld, pc_inc        : out std_logic;
      ir_enA, ir_enD, ir_ld        : out std_logic;
      ir_load, ir_store, ir_add    : in  std_logic;
      ir_neg, ir_halt, ir_branch   : in  std_logic;
      ir_cbranch, ir_iload         : in  std_logic;
      ir_istore, ir_mload, ir_madd : in  std_logic;
      iar_enA, iar_ld              : out std_logic;
      acc_enD, acc_ld, acc_selAlu  : out std_logic;
      alu_accZ                     : in  std_logic;
      alu_op                       : out std_logic_vector(1 downto 0)
      );
  end component;

  signal abus                            : std_logic_vector(15 downto 0);
  signal dbus                            : std_logic_vector(15 downto 0);
  signal mem_enD, mem_rw                 : std_logic;
  signal pc_enA, pc_ld, pc_inc           : std_logic;
  signal ir_enA, ir_enD, ir_ld           : std_logic;
  signal ir_load, ir_store, ir_add       : std_logic;
  signal ir_negate, ir_halt, ir_branch   : std_logic;
  signal ir_cbranch, ir_iload, ir_istore : std_logic;
  signal ir_mload, ir_sub                : std_logic;
  signal iar_enA, iar_ld                 : std_logic;
  signal acc_enD, acc_ld, acc_selAlu     : std_logic;
  signal acc_Q                           : std_logic_vector(15 downto 0);
  signal alu_op                          : std_logic_vector(1 downto 0);
  signal alu_accZ                        : std_logic;
  signal alu_result                      : std_logic_vector(15 downto 0);

begin

  pc : program_counter port map(
    clk=>clk,
    en_A=>pc_enA,
    ld=>pc_ld,
    inc=>pc_inc,
    reset=>reset,
    aBus=>abus,
    dBus=>dbus);


  ir : instruction_register port map(
    clk=>clk,
    en_A=>ir_enA,
    en_D=>ir_enD,
    ld=>ir_ld,
    reset=>reset,
    aBus=>abus,
    dBus=>dbus,
    load=>ir_load,
    store=>ir_store,
    add=>ir_add,
    neg=>ir_negate,
    halt=>ir_halt,
    branch=>ir_branch,
    cbranch=>ir_cbranch,
    iload=>ir_iload,
    istore=>ir_istore,
    dload=>ir_mload,
    dadd=>ir_sub);


  iar : indirect_addr_register port map(
    clk=>clk,
    en_A=>iar_enA,
    ld=>iar_ld,
    reset=>reset,
    aBus=>abus,
    dBus=>dbus);


  acc : accumulator port map(
    clk=>clk,
    en_D=>acc_enD,
    ld=>acc_ld,
    selAlu=>acc_selAlu,
    reset=>reset,
    aluD=>alu_result,
    dBus=>dbus,
    q=>acc_Q);


  aluu : alu port map(
    op=>alu_op,
    accD=>acc_Q,
    dBus=>dbus,
    result=>alu_result,
    accZ=>alu_accZ);


  mem : ram port map(
    r_w=>mem_rw,
    en=>mem_enD,
    reset=>reset,
    aBus=>abus,
    dBus=>dbus);


  ctl : controller port map(
    clk=>clk,
    reset=>reset,
    mem_enD=>mem_enD,
    mem_rw=>mem_rw,
    pc_enA=>pc_enA,
    pc_ld=>pc_ld,
    pc_inc=>pc_inc,
    ir_enA=>ir_enA,
    ir_enD=>ir_enD,
    ir_ld=>ir_ld,
    ir_load=>ir_load,
    ir_store=>ir_store,
    ir_add=>ir_add,
    ir_neg=>ir_negate,
    ir_halt=>ir_halt,
    ir_branch=>ir_branch,
    ir_cbranch=>ir_cbranch,
    ir_iload=>ir_iload,
    ir_istore=>ir_istore,
    ir_mload=>ir_mload,
    ir_madd=>ir_sub,
    iar_enA=>iar_enA,
    iar_ld=>iar_ld,
    acc_enD=>acc_enD,
    acc_ld=>acc_ld,
    acc_selAlu=>acc_selAlu,
    alu_accZ=>alu_accZ,
    alu_op=>alu_op);


  abusX       <= abus;
  dbusX       <= dbus;
  mem_enDX    <= mem_enD;
  mem_rwX     <= mem_rw;
  pc_enAX     <= pc_enA;
  pc_ldX      <= pc_ld;
  pc_incX     <= pc_inc;
  ir_enAX     <= ir_enA;
  ir_enDX     <= ir_enD;
  ir_ldX      <= ir_ld;
  iar_enAX    <= iar_enA;
  iar_ldX     <= iar_ld;
  acc_enDX    <= acc_enD;
  acc_ldX     <= acc_ld;
  acc_selAluX <= acc_selAlu;
  acc_QX      <= acc_Q;
  alu_opX     <= alu_op;
  alu_accZX   <= alu_accZ;
end topArch;

