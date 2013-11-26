class Entry < ActiveRecord::Base
  belongs_to :log, :dependent => :destroy
end

