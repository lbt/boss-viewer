# This is the control file for boss-viewer.
#
# It is a configuration of ruote-kit that doesn't
# spawn a worker thread and runs inside rack

# load json backend
require 'yajl'    # fastest, but uses a c module
# require 'json_pure'  # should work everywhere

require 'ruote-kit'
require 'ruote/storage/fs_storage'

# Load config from boss config areas
boss_route_db=ENV['SERVER_DATABASE']

# Use the correct store type
engine = Ruote::Engine.new(
  Ruote::FsStorage.new(boss_route_db))

# We run under daemontools and it communicates via signals
Signal.trap('SIGTERM') do
  puts 'Shutdown gracefully'
  engine.shutdown
  puts 'Asked engine to stop'
  engine.join
  # Rack doesn't act on SIGTERM
  puts 'Sending SIGINT to stop Rack'
  Process.kill("SIGINT", Process.pid)
end

# establish the RuoteKit engine
RuoteKit.engine = engine

# The catchall is required and must occupy the bottom position.
RuoteKit.engine.register :clear => false do
  # register forces 'override' to false, but postion 'over' overrides that
  # and if matching key ('.+' for catchall) is not in list, it goes to last
  catchall Ruote::StorageParticipant, {'position' => 'over'}
end

use Rack::CommonLogger
use Rack::Lint

run RuoteKit::Application


##################
# Local Variables:
# mode: Ruby;
# End:
