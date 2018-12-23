#!/usr/bin/ruby


TIME_TOKEN_TEMPLATE_SS = "-ss %{token_from}"
TIME_TOKEN_TEMPLATE_TO = "-to %{token_to}"
CMD_TEMPLATE_FF = "ffmpeg -i %{videoclip_ext} %{time_tokens} -q:v 0 -q:a 0 ffavi/%{videoclip_out}"


class FFCommand
	attr_accessor :sstoken, :totoken, :videoclip, :destext

	def initialize(_sstoken, _totoken, _videoclip, _destext)
		@sstoken = _sstoken
		@totoken = _totoken
		@videoclip = _videoclip
		@destext = _destext
	end
	
	def change_ext
		corename = @videoclip.to_s.split(".")[0]
		corename + "." +  @destext.to_s
	end

	def make_tokens
		time_tokens = []
		if @sstoken.relevant?
			time_tokens << TIME_TOKEN_TEMPLATE_SS % {token_from: @sstoken.value}
		end
		if @totoken.relevant?
			time_tokens << TIME_TOKEN_TEMPLATE_TO % {token_to: @totoken.value}
		end
		time_tokens.join(" ")
	end

	def fill_command
		filling = {videoclip_ext: @videoclip,
	     		   time_tokens: make_tokens,
			   videoclip_out: change_ext
			  }
		CMD_TEMPLATE_FF % filling
	end

	def to_s
		fill_command
	end

end


CMD_TEMPLATE_RM = "rm %{videoclip}"

class RMCommand
	attr_accessor :videoclip

	def initialize(_videoclip)
		@videoclip = _videoclip
	end

	def fill_command
		CMD_TEMPLATE_RM % {videoclip: @videoclip}
	end

	def to_s
		fill_command
	end

end


class TimeToken
	attr_reader :value, :relevant

	def initialize(_value = "")
		@value = _value
		@relevant = false
		unless @value.nil? or @value.empty? or @value.scan(/[^0]/).empty?
			@relevant = true
		end
	end

	def relevant?
		@relevant
	end

	def ==(other)
		@value == other.value and @relevant == other.relevant
	end

end


#cmd types
:rm
:ff

RM_STR = "rm"

class InvalidTokenstringError < StandardError
end

class InputParser
	attr_reader :argsarray

	def initialize(_argsarray)
		@argsarray = _argsarray
	end

	def tokenstring_valid?(_ts)
		_ts.scan(/[^0123456789:]/).empty?
	end

	def process
		case @argsarray.length
		when 1
			[:ff, TimeToken.new, TimeToken.new]
		when 2
			if @argsarray[1].eql?(RM_STR)
				[:rm, TimeToken.new, TimeToken.new]
			else	
				raise InvalidTokenstringError unless tokenstring_valid?(@argsarray[1])
				[:ff, TimeToken.new(@argsarray[1]), TimeToken.new]
			end
		when 3
			raise InvalidTokenstringError unless tokenstring_valid?(@argsarray[1])
			raise InvalidTokenstringError unless tokenstring_valid?(@argsarray[2])
			[:ff, TimeToken.new(@argsarray[1]), TimeToken.new(@argsarray[2])]
		end
	end
end



def argv_valid?(argv)
	argv.length > 0 and argv.length <= 3
end

def print_usage
	puts 
	puts "    #{$PROGRAM_NAME}  input_file               # caly              ()"
	puts "    #{$PROGRAM_NAME}  input_file  rm           # wypada"
	puts "    #{$PROGRAM_NAME}  input_file  XX           # od XX do konca    (-ss)"
	puts "    #{$PROGRAM_NAME}  input_file  XX YY        # od XX do YY       (-ss -to)"
	puts "    #{$PROGRAM_NAME}  input_file   0 YY        # od poczatku do YY (-to)"
	puts
end

def get_cmd(argv)
	parsed = InputParser.new(argv).process
	case parsed[0]
	when :rm
		RMCommand.new(argv[0]).fill_command
	when :ff
		FFCommand.new(parsed[1], parsed[2], argv[0], "avi").fill_command
	end
end


unless argv_valid?(ARGV)
	print_usage
	exit
end

puts get_cmd(ARGV)
