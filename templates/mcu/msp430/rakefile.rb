require 'rake/clean'
require 'optparse'

##############################################
## Parse Linker File
##############################################
# Toolchain was installed in the docker image under $/usr/toolchain
DEV_NAME = ENV['DEVICE']

LINKER_CMD_FILE = "/usr/toolchain/ccs_base/msp430/include/lnk_#{DEV_NAME.downcase}.cmd"

puts "Linker file: #{LINKER_CMD_FILE}"

##############################################
## Define Compiler/linker Variables 
##############################################
TOOLCHAIN_PATH = "/usr/toolchain"
COMPILER_PATH =  "/usr/toolchain/ti-cgt-msp430_20.2.2.LTS"


SOURCE_DIR  = "src"
INCLUDE_DIR = "include/"
OBJ_DIR     = "build/obj"
BUILD_DIR   = "build"
GCC         = "#{COMPILER_PATH}/bin/cl430" 


DEVICE      = "__#{DEV_NAME.upcase}__"


FileUtils.mkdir_p "#{OBJ_DIR}/"
FileUtils.mkdir_p "#{BUILD_DIR}/"


SOURCES     = Rake::FileList["#{SOURCE_DIR}/*.c"]
OBJECTS     = SOURCES.ext(".obj").pathmap("#{OBJ_DIR}/%f")
INCLUDES    = INCLUDE_DIR

TARGET      = "#{BUILD_DIR}/#{File.basename(File.dirname(__FILE__))}_#{Time.now.strftime("%Y%m%d_%H%M")}"

STATIC_LIBS     = "-llibmath.a -llibc.a"
LIBS            = "#{LINKER_CMD_FILE} #{STATIC_LIBS}"


INCLUDE_PATHS = " \
                --include_path=\"#{TOOLCHAIN_PATH}/ccs_base/msp430/include\"  \
                --include_path=#{INCLUDES}  \
                --include_path=\"#{COMPILER_PATH}/include\" \
                " 


INCLUDE_LIBS_PATH = " \
                    -i\"#{TOOLCHAIN_PATH}/ccs_base/msp430/include\" \
                    -i\"#{TOOLCHAIN_PATH}/ccs_base/msp430/lib/5xx_6xx_FRxx\"    \
                    -i\"#{COMPILER_PATH}/lib\"  \
                    -i\"#{COMPILER_PATH}/include\" \
                    "

COMPILER_OPTS   = "-vmspx --use_hw_mpy=F5 -O2 -g --c99 --define=#{DEVICE}"

MEMORY_MAP  = "#{BUILD_DIR}/memory.map"
LINKER_OPTS = "--run_linker --heap_size=160 --stack_size=160 -m#{MEMORY_MAP}"
LINKER_OUTPUT_OPTS  = "" #"--xml_link_info=\"#{TARGET}.xml\""


MISC_OPTS           = "--advice:power=\"all\" --advice:hw_config=\"all\"" 
DIAGNOSTIC_OPTS     = "--diag_warning=255 --diag_wrap=off --display_error_number --warn_sections"
RUNTIME_ENV_OPTS    = "--cinit_hold_wdt=on --rom_model"
RUNTIME_MODEL_OPTS  = "--printf_support=nofloat --silicon_errata=CPU21 --silicon_errata=CPU22 --silicon_errata=CPU40"
FILE_SEARCH_PATH_OPTS   = "--reread_libs"


CFLAGS = "#{COMPILER_OPTS} #{MISC_OPTS} #{RUNTIME_MODEL_OPTS}"
LFLAGS = "#{LINKER_OPTS} #{RUNTIME_ENV_OPTS} #{DIAGNOSTIC_OPTS} #{FILE_SEARCH_PATH_OPTS} #{LINKER_OUTPUT_OPTS}"


##############################################
## Ruby Tools on Docker
##############################################
require_relative "/usr/toolchain/tools/RakeSupportFunctions"
include RakeSupportFunctions

##############################################
## Building Process
##############################################
task :default => :build

task :build => OBJECTS do
    puts "#{BBlue}[Linking]#{Color_Off}\n"
    quiet_sh "#{GCC} #{CFLAGS} #{LFLAGS} #{INCLUDE_LIBS_PATH} -o #{TARGET}.out #{OBJECTS} #{LIBS}"

end


# %f The base filename of the path, with its file extension,
# pathmap :Apply the pathmap spec to each of the included file names, returning a new file list with the modified paths. (See String#pathmap for details.)
#  lambda:     say_something = -> { puts "This is a lambda" }

# For each '.o' file add path "SOURCE_DIR/ " and change extension to C
rule '.obj' => ->(t){t.pathmap("#{SOURCE_DIR}/%f").ext(".c")} do |task|
    puts "#{BBlue}[Building Object] #{task.name} #{Color_Off} \n"
    quiet_sh "#{GCC} #{CFLAGS}  #{INCLUDE_PATHS} --preproc_with_compile --preproc_dependency=#{task.name.ext(".d_raw")} --obj_directory=#{OBJ_DIR}/ #{task.source} #{COLOR_OUTPUT} " 

end

CLEAN.include("#{OBJ_DIR}", "#{BUILD_DIR}" )


