require "spec_helper"
require "wycinacz"




describe FFCommand do

	it "has tokens" do
		cmd = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expect(cmd.sstoken.value).to eq("11")
		expect(cmd.totoken.value).to eq("22")
		expect(cmd.videoclip).to eq("hipoa.mp4")
	end

	it "has no tokens" do
		cmd = FFCommand.new(TimeToken.new, TimeToken.new, "hipoa.mp4", "avi")
		expect(cmd.sstoken.relevant?).to be false
		expect(cmd.totoken.relevant?).to be false
	end

	it "changes exts" do
		cmd1 = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expect(cmd1.change_ext).to eq "hipoa.avi"
		cmd2 = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "cokolwiek.mp4", "avi")
		expect(cmd2.change_ext).to eq "cokolwiek.avi"
	end

	it "assembles timing tokens from two" do
		cmd1 = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expect(cmd1.make_tokens).to eq("-ss 11 -to 22")
		cmd2 = FFCommand.new(TimeToken.new("33"), TimeToken.new("44"), "hipoa.mp4", "avi")
		expect(cmd2.make_tokens).to eq("-ss 33 -to 44")
	end

	it "assembles timing tokens from one" do
		cmd1 = FFCommand.new(TimeToken.new("11"), TimeToken.new, "hipoa.mp4", "avi")
		expect(cmd1.make_tokens).to eq("-ss 11")
		cmd2 = FFCommand.new(TimeToken.new, TimeToken.new("44"), "hipoa.mp4", "avi")
		expect(cmd2.make_tokens).to eq("-to 44")
	end

	it "assembles timing tokens from none" do
		cmd1 = FFCommand.new(TimeToken.new, TimeToken.new, "hipoa.mp4", "avi")
		expect(cmd1.make_tokens).to eq("")
	end

	it "assembles timing tokens from zeros" do
		cmd1 = FFCommand.new(TimeToken.new("0"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expect(cmd1.make_tokens).to eq("-to 22")
		cmd2 = FFCommand.new(TimeToken.new("33"), TimeToken.new("0"), "hipoa.mp4", "avi")
		expect(cmd2.make_tokens).to eq("-ss 33")
		cmd3 = FFCommand.new(TimeToken.new("0"), TimeToken.new("0"), "hipoa.mp4", "avi")
		expect(cmd3.make_tokens).to eq("")
	end

	it "fills command template 1" do
		cmd1 = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expected1 = "ffmpeg -i hipoa.mp4 -ss 11 -to 22 -q:v 0 -q:a 0 ffavi/hipoa.avi"
		expect(cmd1.fill_command).to eq(expected1)
	end

	it "fills command template 2" do
		cmd1 = FFCommand.new(TimeToken.new("33"), TimeToken.new("44"), "nalesnik.mp4", "avi")
		expected1 = "ffmpeg -i nalesnik.mp4 -ss 33 -to 44 -q:v 0 -q:a 0 ffavi/nalesnik.avi"
		expect(cmd1.fill_command).to eq(expected1)
	end

	it "overrides to_s" do
		cmd1 = FFCommand.new(TimeToken.new("11"), TimeToken.new("22"), "hipoa.mp4", "avi")
		expected1 = "ffmpeg -i hipoa.mp4 -ss 11 -to 22 -q:v 0 -q:a 0 ffavi/hipoa.avi"
		expect(cmd1.to_s).to eq(expected1)
	end

end



describe RMCommand do
	it "fills command template 1" do
		cmd = RMCommand.new("hipoa.mp4")
		expect(cmd.fill_command).to eq("rm hipoa.mp4")
	end
	it "fills command template 2" do
		cmd = RMCommand.new("nalesnik.mp4")
		expect(cmd.fill_command).to eq("rm nalesnik.mp4")
	end
	it "overrides to_s" do
		cmd = RMCommand.new("nalesnik.mp4")
		expect(cmd.to_s).to eq("rm nalesnik.mp4")
	end
end


describe TimeToken do
	it "is relevant" do
		tt_good = TimeToken.new("1:23:45")
		expect(tt_good.relevant?).to be true
		tt_bad1 = TimeToken.new("")
		expect(tt_bad1.relevant?).to be false
		tt_bad2 = TimeToken.new
		expect(tt_bad2.relevant?).to be false
	end

	it "is not relevant if zero" do
		expect(TimeToken.new("0").relevant?).to be false
		expect(TimeToken.new("00").relevant?).to be false
		expect(TimeToken.new("000").relevant?).to be false
	end


	it "equals" do
		tt1 = TimeToken.new("1:23:45")
		tt2 = TimeToken.new("1:23:45")
		tt3 = TimeToken.new("12")
		expect(tt1).to eq(tt2)
		expect(tt1).not_to eq(tt3)
		expect(tt2).not_to eq(tt3)
	end

	it "array equals" do
		tt1 = TimeToken.new("1:23:45")
		tt2 = TimeToken.new("1:23:45")
		tt3 = TimeToken.new("00")
		arr = [TimeToken.new("1:23:45"), TimeToken.new("1:23:45")]
		expect([tt1, tt2]).to eq(arr)
		expect([tt2, tt3]).not_to eq(arr)
	end

	it "irrelevant equals" do
		tt_bad1 = TimeToken.new("")
		tt_bad2 = TimeToken.new
		expect(tt_bad1).to eq(tt_bad2)
		expect([TimeToken.new(""), TimeToken.new("")]).to eq ([TimeToken.new, TimeToken.new])
		expect([TimeToken.new(""), TimeToken.new]).to eq ([TimeToken.new, TimeToken.new("")])
	end


end

#cmd types
:rm
:ff

describe InputParser do
	it "validates token string" do
		ip = InputParser.new([])
		expect(ip.tokenstring_valid?(       "1")).to be true
		expect(ip.tokenstring_valid?(      "00")).to be true
		expect(ip.tokenstring_valid?(    "1:23")).to be true
		expect(ip.tokenstring_valid?(   "00:23")).to be true
		expect(ip.tokenstring_valid?( "1:23:45")).to be true
		expect(ip.tokenstring_valid?("00:23:45")).to be true

		expect(ip.tokenstring_valid?(       "a")).to be false
		expect(ip.tokenstring_valid?( "1;23;45")).to be false
		expect(ip.tokenstring_valid?( "1-23:45")).to be false
	end

	it "gets one argument" do
		ip = InputParser.new(["input_file.mp4"])
		expect(ip.process).to eq([:ff, TimeToken.new, TimeToken.new])
	end

	it "gets two args: RM" do
		ip = InputParser.new(["input_file.mp4", "rm"])
		expect(ip.process).to eq([:rm, TimeToken.new, TimeToken.new])
	end

	it "gets two args: non-RM" do
		ip = InputParser.new(["input_file.mp4", "1:23"])
		expect(ip.process).to eq([:ff, TimeToken.new("1:23"), TimeToken.new])
	end

	it "gets two args: bullshit" do
		ip = InputParser.new(["input_file.mp4", "bullshit"])
		expect {ip.process}.to raise_error(InvalidTokenstringError) 
	end

	it "gets three args" do
		ip = InputParser.new(["input_file.mp4", "1:23", "4:56"])
		expect(ip.process).to eq([:ff, TimeToken.new("1:23"), TimeToken.new("4:56")])
		ip0 = InputParser.new(["input_file.mp4", "0", "4:56"])
		expect(ip0.process).to eq([:ff, TimeToken.new("0"), TimeToken.new("4:56")])
	end

	it "gets three args: bullshit" do
		ip1 = InputParser.new(["input_file.mp4", "bullshit", "4:56"])
		expect {ip1.process}.to raise_error(InvalidTokenstringError) 
		ip2 = InputParser.new(["input_file.mp4", "1:23", "bullshit"])
		expect {ip2.process}.to raise_error(InvalidTokenstringError) 
	end
end

describe '#get_cmd' do
	it "produces command out of initial args" do
		expect(get_cmd(["mucha.mp4"])).to eq("ffmpeg -i mucha.mp4  -q:v 0 -q:a 0 ffavi/mucha.avi")
		expect(get_cmd(["mucha.mp4", "rm"])).to eq("rm mucha.mp4")
		expect(get_cmd(["mucha.mp4", "12"])).to eq("ffmpeg -i mucha.mp4 -ss 12 -q:v 0 -q:a 0 ffavi/mucha.avi")
		expect(get_cmd(["mucha.mp4", "12", "34:56"])).to eq("ffmpeg -i mucha.mp4 -ss 12 -to 34:56 -q:v 0 -q:a 0 ffavi/mucha.avi")
		expect(get_cmd(["mucha.mp4",  "0", "34:56"])).to eq("ffmpeg -i mucha.mp4 -to 34:56 -q:v 0 -q:a 0 ffavi/mucha.avi")
	end
end
